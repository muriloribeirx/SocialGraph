import pytest

import crossref_edges as cr


def test_resolve_to_doi_with_doi():
    assert cr.resolve_to_doi('10.1000/xyz') == '10.1000/xyz'


def test_resolve_to_doi_search(monkeypatch):
    called = {}

    def fake_search(title, rows=3):
        called['q'] = title
        return [{'DOI': '10.1111/fake.doi'}]

    monkeypatch.setattr(cr, 'search_doi_by_title', fake_search)
    doi = cr.resolve_to_doi('A test title')
    assert doi == '10.1111/fake.doi'
    assert called['q'] == 'A test title'


def test_get_references_for_work(monkeypatch):
    # fake get_work_by_doi to include a 'reference' list
    fake = {'reference': [{'DOI': '10.1/one'}, {'doi': '10.2/two'}, {'unrelated': 'no-doi'}]}

    monkeypatch.setattr(cr, 'get_work_by_doi', lambda doi: fake)
    refs = cr.get_references_for_work('10.12345/test')
    assert refs == ['10.1/one', '10.2/two']


def test_get_references_with_unstructured_doi(monkeypatch):
    fake = {'reference': [{'unstructured': 'Smith J. (2020) Interesting paper. DOI: 10.1234/abc-2020'}, {'unstructured': 'No DOI here'}]}
    monkeypatch.setattr(cr, 'get_work_by_doi', lambda doi: fake)
    refs = cr.get_references_for_work('10.12345/test')
    assert '10.1234/abc-2020' in refs


def test_get_work_by_doi_uses_encoded_path(monkeypatch):
    observed = {}

    class FakeResp:
        def __init__(self, status_code=404, json_data=None):
            self.status_code = status_code
            self._json = json_data or {}

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError()

        def json(self):
            return self._json

    def fake_get(url, headers=None, timeout=None):
        observed['url'] = url
        return FakeResp(status_code=404)

    monkeypatch.setattr(cr.requests, 'get', fake_get)
    cr.get_work_by_doi('10.1016/j.inffus.2019.12.012')
    assert '%2F' in observed['url'] and '10.1016%2Fj.inffus.2019.12.012' in observed['url']


def test_get_citers_for_work_uses_encoded_path(monkeypatch):
    observed = {}

    class FakeResp:
        def __init__(self, status_code=200, json_data=None):
            self.status_code = status_code
            self._json = json_data or []

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError()

        def json(self):
            return self._json

    def fake_get(url, headers=None, timeout=None):
        observed['url'] = url
        return FakeResp(status_code=200, json_data=[])

    monkeypatch.setattr(cr.requests, 'get', fake_get)
    cr.get_citers_for_work('10.1016/j.inffus.2019.12.012')
    assert '%2F' in observed['url'] and '10.1016%2Fj.inffus.2019.12.012' in observed['url']


def test_gerar_edges_crossref_bfs(monkeypatch):
    # construct graph: A -> B -> C and A -> D -> C
    # map title resolution to DOIs
    monkeypatch.setattr(cr, 'resolve_to_doi', lambda x: x.lower())

    # adjacency mapping
    adj = {
        'a': ['b', 'd'],
        'b': ['c'],
        'd': ['c'],
        'c': []
    }

    monkeypatch.setattr(cr, 'get_references_for_work', lambda doi: adj.get(doi, []))

    edges = cr.gerar_edges_crossref('a', 'c', max_depth=3, max_paths=2)
    # edges should include ('a','b'),('b','c') and/or ('a','d'),('d','c') - order may vary
    assert (('a', 'b') in edges and ('b', 'c') in edges) or (('a', 'd') in edges and ('d', 'c') in edges)


def test_gerar_edges_crossref_incoming(monkeypatch):
    # test BFS in incoming direction: who cites whom
    monkeypatch.setattr(cr, 'resolve_to_doi', lambda x: x.lower())
    # incoming graph: X <- A <- B  (A is cited by X), and X <- D <- B etc
    # we'll model adjacency for citers: for a given node, get_citers_for_work returns items that cite it
    adj_in = {
        'c': ['b'],
        'b': ['a'],
        'a': ['x'],
        'x': []
    }

    monkeypatch.setattr(cr, 'get_citers_for_work', lambda doi: adj_in.get(doi, []))

    edges = cr.gerar_edges_crossref('c', 'a', max_depth=4, max_paths=2, direction='incoming')
    # we expect edges representing path c <- b <- a to be returned as tuples of DOIs (cited->citer)
    # since gerar_edges_crossref returns edges as (p[i], p[i+1]), this will be ('c','b'), ('b','a')
    assert ('c', 'b') in edges and ('b', 'a') in edges
