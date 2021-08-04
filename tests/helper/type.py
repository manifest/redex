from typing import Any, Sequence
from hypothesis import strategies as st


def any():
    return st.none() | st.booleans() | st.integers() | st.binary() | st.text()


def seq_butnot_tuple():
    return st.lists(any()) | st.sets(any())


def annotation_butnot_tuple():
    return (
        st.just(Any)
        | st.just(None)
        | st.just(True)
        | st.just(False)
        | st.just(Sequence[Any])
        | st.just(Sequence[tuple[Any, ...]])
    )
