from typing import Iterator, Tuple, Any, Dict, TypeAlias, List

JSONTask: TypeAlias = Dict[str, List[Dict[str, List[List[int]]]]]
Sample: TypeAlias = Tuple[str, JSONTask]
Grid = List[List[int]]
GridPairs: TypeAlias = List[Dict[str, List[List[int]]]]
