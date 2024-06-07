-- Sample SQL to update data with actual results
UPDATE election_results
SET
    electors = actual_results.electors,
    total_votes = actual_results.total_votes,
    turnout_percentage = actual_results.turnout_percentage,
    elected_member = actual_results.elected_member,
    elected_party = actual_results.elected_party,
    local_alliance = actual_results.local_alliance,
    vote_share_percentage = actual_results.vote_share_percentage,
    margin = actual_results.margin
FROM
    (VALUES
        (2024, 1, 'Kasaragod', 1463106, 1112546, 76.04, 'Rajmohan Unnithan', 'INC', 'UDF', 44.10, 100649),
        (2024, 2, 'Kannur', 1377872, 1063855, 77.21, 'K. Sudhakaran', 'INC', 'UDF', 48.74, 108982),
        (2024, 3, 'Vatakara', 1432148, 1122947, 78.41, 'Shafi Parambil', 'INC', 'UDF', 49.65, 114506),
        (2024, 4, 'Wayanad', 1474314, 1084653, 73.57, 'Rahul Gandhi', 'INC', 'UDF', 59.69, 364422),
        (2024, 5, 'Kozhikode', 1443392, 1090050, 75.52, 'MK Raghavan', 'INC', 'UDF', 47.74, 146176),
        (2024, 6, 'Malappuram', 1487570, 1085182, 72.95, 'ET Mohammed Basheer', 'IUML', 'UDF', 59.35, 300118),
        (2024, 7, 'Ponnani', 1480092, 1026296, 69.34, 'Abdussamad Samadani', 'IUML', 'UDF', 54.81, 235760),
        (2024, 8, 'Palakkad', 1407960, 1035836, 73.57, 'VK Sreekandan', 'INC', 'UDF', 40.66, 75283),
        (2024, 9, 'Alathur (SC)', 1351496, 992268, 73.42, 'K. Radhakrishnan', 'CPI(M)', 'LDF', 40.66, 20111),
        (2024, 10, 'Thrissur', 1496401, 1090876, 72.9, 'Suresh Gopi', 'BJP', 'NDA', 37.80, 74686),
        (2024, 11, 'Chalakudy', 1322334, 951287, 71.94, 'Benny Behanan', 'INC', 'UDF', 41.44, 63754),
        (2024, 12, 'Ernakulam', 1333287, 910502, 68.29, 'Hibi Eden', 'INC', 'UDF', 52.97, 250385),
        (2024, 13, 'Idukki', 1263196, 840657, 66.55, 'Dean Kuriakose', 'INC', 'UDF', 51.43, 133727),
        (2024, 14, 'Kottayam', 1274536, 836223, 65.61, 'Francis George', 'KEC', 'UDF', 43.60, 87266),
        (2024, 15, 'Alappuzha', 1410664, 1058703, 75.05, 'KC Venugopal', 'INC', 'UDF', 38.21, 63513),
        (2024, 16, 'Mavelikara (SC)', 1357045, 894971, 65.95, 'Kodikunnil Suresh', 'INC', 'UDF', 41.29, 10868),
        (2024, 17, 'Pathanamthitta', 1451111, 919569, 63.37, 'Anto Antony', 'INC', 'UDF', 39.98, 66119),
        (2024, 18, 'Kollam', 1343640, 915691, 68.15, 'NK Premachandran', 'RSP', 'UDF', 48.45, 150302),
        (2024, 19, 'Attingal', 1418165, 985341, 69.48, 'Adoor Prakash', 'INC', 'UDF', 33.29, 684),
        (2024, 20, 'Thiruvananthapuram', 1448748, 962983, 66.47, 'Shashi Tharoor', 'INC', 'UDF', 37.19, 16077) 
    ) AS actual_results(year, constituency_number, constituency_name, electors, total_votes, turnout_percentage, elected_member, elected_party, local_alliance, vote_share_percentage, margin)
WHERE
    election_results.year = actual_results.year
    AND election_results.constituency_number = actual_results.constituency_number;
