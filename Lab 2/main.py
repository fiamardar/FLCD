from SymbolTable import SymbolTable

if __name__ == '__main__':
    st = SymbolTable()
    id_a = st.add("a")
    id_b = st.add("b")
    id_23 = st.add("23")
    id_32 = st.add("32")

    assert st.search("a") == id_a
    assert st.add("a") == id_a
    assert st.delete("c") is None
    assert st.delete("a") == id_a
    assert st.search("a") is False
    assert st.add("a") == id_a
    assert st.search("23")[0] == st.search("32")[0]


