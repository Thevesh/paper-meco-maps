# Progress Tracker

| Unit | Year | Parlimen GeoJSON | DUN GeoJSON | Validation | Parlimen Cartogram (Equal) | Parlimen Cartogram (Electorate) | DUN Cartogram (Equal) | DUN Cartogram (Electorate) |
|------|------|-----------------|------------|------------|--------------------------|-----------------------------|---------------------|-------------------------|
| Peninsular | 1955 | ✅ | n/a | ✅ | ❌ | ❌ | - | - |
| Peninsular | 1959 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Peninsular | 1974 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Peninsular | 1984 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Peninsular | 1994 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Peninsular | 2003 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Peninsular | 2018 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 1966 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 1974 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 1984 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 1994 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 2003 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sabah | 2019 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 1968 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 1977 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 1987 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 1996 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 2005 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Sarawak | 2015 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |


## Methodology Notes
- `peninsular_1959_parlimen`: Constituencies are numbered according to the map presented in the election report (beginning with Perlis), rather than the order in which the data was reported (beginning with Johor). This is both because the map explicitly numbers the constituencies (the data section does not), as well as because the map is consistent with the numbering methodology in future years. In any case, both represent a change in ordering methodology relative to 1955, where Penang came first (followed by Malacca). 
- `peninsular_1959_dun`: Same ordering issue as above, with same solution.
- `peninsular_1959_dun`: There are 2 seats where there is inconsistency between the results data and the map in the same report. We choose the option which generates consistency with future names, to avoid requiring a separate map for 1964 purely due to renaming. Cases: We write Kangar Town as Bandar Kangar, and Kelawai as Kelawei. In both cases, the name chosen is consistent with the election reports for 1964 and 1969.
- `peninsular_2003_parlimen`: This is the first map where P.125 Putrajaya appears. However, P.125 Putrajaya was actually carved out of Dengkil in 2001. In this collection, it is presented together with the 2003 redelineation of Peninsular Malaysia, as there was no other election between 2001 and 2003 that would create a practical need to have two versions of the map.
- `sabah_2019`: The redelineation was completed by SPR in 2017, but was only tabled in Parliament in 2019.

## To Check:
- `peninsular_1984_dun`: Sungai Pelek or Sungai Pelik (as discussed in Telegram)
