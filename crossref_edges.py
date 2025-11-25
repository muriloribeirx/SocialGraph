import requests
import requests_cache
from urllib.parse import quote
from collections import deque
import time
import re

# Simple cache to avoid hammering CrossRef during development/tests
requests_cache.install_cache('crossref_cache', expire_after=24 * 3600)

CROSSREF_API = "https://api.crossref.org"
USER_AGENT = "SocialGraphCrossRef/1.0 (mailto:you@example.com)"


def search_doi_by_title(title, rows=5):
    """Search CrossRef by title and return candidate items.

    Returns list of CrossRef work items (message.items)
    """
    url = f"{CROSSREF_API}/works?query.title={quote(title)}&rows={rows}"
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    resp.raise_for_status()
    data = resp.json().get('message', {})
    print(f"Search for title '{title}' returned {data.get('total-results', 0)} results")
    return data.get('items', [])


def get_work_by_doi(doi):
    doi = doi.lower()
    # DOIs include / and other chars — encode fully when used in a path
    url = f"{CROSSREF_API}/works/{quote(doi, safe='')}"
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get('message')


def get_references_for_work(doi):
    """Return list of DOIs referenced by given DOI.

    If references lack DOI, they are skipped (best-effort mapping could be added).
    """
    work = get_work_by_doi(doi)
    if not work:
        return []
    refs = work.get('reference', []) or []
    dois = []
    for ref in refs:
        rdoi = ref.get('DOI') or ref.get('doi') or None

        # if there is no DOI, attempt to extract from 'unstructured'/reference string
        if not rdoi:
            txt = None
            # CrossRef sometimes supplies 'unstructured' or 'article-title' etc
            for key in ('unstructured', 'article-title', 'literal'):
                if key in ref and ref[key]:
                    txt = ref[key]
                    break

            if txt:
                # DOI pattern: 10.<digits>/<non-space>
                m = re.search(r"\b10\.\d{4,9}/[^\s'\"<>]+\b", txt, flags=re.I)
                if m:
                    rdoi = m.group(0)

        if rdoi:
            dois.append(rdoi.lower())
    # use dict to preserve order and uniq
    return list(dict.fromkeys(dois))


def get_citers_for_work(doi):
    """Return list of DOIs that cite the given DOI using OpenCitations COCI.

    Falls back to an empty list on errors. The OpenCitations endpoint returns
    rows of citation objects which include a 'citing' DOI.
    """
    try:
        # encode slash and other characters in DOI for the URL path
        url = f"https://opencitations.net/index/api/v1/citations/DOI:{quote(doi, safe='')}"
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        data = resp.json() or []
        citers = []
        for item in data:
            # OpenCitations usually returns 'citing' as the key for the citing DOI
            d = item.get('citing') or item.get('citing_doi') or item.get('citingWork')
            if d:
                citers.append(d.lower())
        return list(dict.fromkeys(citers))
    except Exception:
        # be conservative and return empty if external service fails
        return []


def resolve_to_doi(name_or_doi):
    """Resolve an input which may already be a DOI or a human title.

    Returns normalized DOI string or None.
    """
    if not name_or_doi:
        return None
    s = name_or_doi.strip()
    if s.lower().startswith('10.'):
        return s.lower()

    # try search
    try:
        candidates = search_doi_by_title(s, rows=3)
        if candidates:
            # pick best candidate (first) — could be improved with scoring
            doi = candidates[0].get('DOI')
            if doi:
                return doi.lower()
    except Exception:
        # swallow network/errors and return None
        return None
    return None


def gerar_edges_crossref(start_title_or_doi, end_title_or_doi, max_depth=3, max_paths=5, max_expand_per_node=40, direction='incoming'):
    """BFS search over CrossRef references to find paths between two works.

    Returns a list of edges as tuples (a, b) where nodes are DOIs.
    This is designed to return the same shape as existing wikipedia_edges. If you
    pass paper titles they'll be resolved to DOIs where possible.
    """
    start = resolve_to_doi(start_title_or_doi)
    end = resolve_to_doi(end_title_or_doi)
    if not start or not end:
        raise ValueError('start or end could not be resolved to DOI')

    queue = deque([(start, [start])])
    found_paths = []
    visited = set([start])

    while queue and len(found_paths) < max_paths:
        current, path = queue.popleft()
        depth = len(path) - 1
        if depth >= max_depth:
            continue

        try:
            if direction == 'incoming':
                neighbors = get_citers_for_work(current)
            else:
                neighbors = get_references_for_work(current)
            print(f"Neighbors of {current}: {neighbors}")
        except Exception:
            # simple backoff for transient errors
            time.sleep(0.5)
            neighbors = []

        # limit neighbors to avoid explosion
        neighbors = neighbors[:max_expand_per_node]

        for nb in neighbors:
            if nb in path:
                continue
            new_path = path + [nb]
            if nb == end:
                found_paths.append(new_path)
                if len(found_paths) >= max_paths:
                    break
            else:
                if len(new_path) <= max_depth + 1:
                    queue.append((nb, new_path))

        # polite pause
        time.sleep(0.05)

    # flatten to unique edges
    edges = []
    seen = set()
    print(f"Found {len(found_paths)} paths")
    for p in found_paths:
        for i in range(len(p) - 1):
            edge = (p[i], p[i + 1])
            if edge not in seen:
                edges.append(edge)
                seen.add(edge)

    return edges


if __name__ == '__main__':
    # quick smoke test (no network tests here)
    print('crossref_edges module loaded')
