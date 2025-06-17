# Coverage (Delimitations)

| Unit | Year | Parlimen GeoJSON | DUN GeoJSON | Validation |
|------|------|-----------------|------------|------------|
| Peninsular | 1955 | ✅ | n/a | ✅ |
| Peninsular | 1959 | ✅ | ✅ | ✅ |
| Peninsular | 1974 | ✅ | ✅ | ✅ |
| Peninsular | 1984 | ✅ | ✅ | ✅ |
| Peninsular | 1994 | ✅ | ✅ | ✅ |
| Peninsular | 2003 | ❌ | ❌ | ❌ |
| Peninsular | 2018 | ✅ | ✅ | ✅ |
| Sabah | 1966 | ✅ | ✅ | ✅ |
| Sabah | 1974 | ✅ | ✅ | ✅ |
| Sabah | 1984 | ✅ | ✅ | ✅ |
| Sabah | 1994 | ✅ | ✅ | ✅ |
| Sabah | 2003 | ✅ | ✅ | ✅ |
| Sabah | 2019 | ✅ | ✅ | ✅ |
| Sarawak | 1968 | ✅ | ✅ | ✅ |
| Sarawak | 1977 | ✅ | ✅ | ✅ |
| Sarawak | 1987 | ✅ | ✅ | ✅ |
| Sarawak | 1996 | ✅ | ✅ | ✅ |
| Sarawak | 2005 | ❌ | ❌ | ❌ |
| Sarawak | 2015 | ✅ | ✅ | ✅ |

The base delimitations are the 'single source of truth' from which the following are programatically generated:
- Election-specific maps, i.e. a single map with the right delimitation (for state elections) or combination of delimiations (for federal elections)
- Equally-weighted Dorling cartograms, which accord the same area to every seat on a map; useful for visualising the composition of Parliament / DUN in a way that still retains its spatial link.
- Electorate-weighted Dorling cartograms, which accord area in proportion to the number of registered voters; useful for visualising continuous or categorical outcome variables (voter turnout, rejected votes, majorities, winning party) in a manner that correctly visualises its true incidence (land doesn't vote, people do).


## Methodology Notes
- `peninsular_1959_parlimen`: Constituencies are numbered according to the map presented in the election report (beginning with Perlis), rather than the order in which the data was reported (beginning with Johor). This is both because the map explicitly numbers the constituencies (the data section does not), as well as because the map is consistent with the numbering methodology in future years. In any case, both represent a change in ordering methodology relative to 1955, where Penang came first (followed by Malacca). 
- `peninsular_1959_dun`: Same ordering issue as above, with same solution.
- `peninsular_1959_dun`: We follow the names used on the map rather than reports in 2 cases: Bandar Kangar (Kangar Town in 1959 report, changed in 1964), and Kelawai (Kelewei in 1959,64,69 reports).
- `peninsular_2003_parlimen`: This is the first map where P.125 Putrajaya appears. However, P.125 Putrajaya was actually carved out of Dengkil in 2001. In this collection, it is presented together with the 2003 redelineation of Peninsular Malaysia, as there was no other election between 2001 and 2003 that would create a practical need to have two versions of the map.
- `sabah_2019`: The redelineation was completed by SPR in 2017, but was only tabled in Parliament in 2019. We name the file as `_2019` rather than `_2017` to make more intuitive to understand when the map should be used.
