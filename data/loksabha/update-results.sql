-- Sample SQL to update data with actual results
UPDATE election_results
SET
    electors = actual_results.electors,
    total_votes = actual_results.total_votes,
    turnout_percentage = actual_results.turnout_percentage,
    elected_member = actual_results.elected_member,
    elected_party = actual_results.elected_party,
    vote_share_percentage = actual_results.vote_share_percentage,
    margin = actual_results.margin
FROM
    (VALUES
        (2024, 1, 'Kasaragod', 197186, 160524, 81.41, 'Rajmohan Unnithan', 'INC', 0.0, 12234),
        (2024, 2, 'Kannur', 181591, 172669, 95.09, 'K. Sudhakaran', 'INC', 0.0, 47267),
        (2024, 3, 'Vatakara', 172661, 168154, 97.39, 'Shafi Parambil', 'INC', 0.0, 54957),
        (2024, 4, 'Wayanad', 144743, 121313, 83.81, 'Rahul Gandhi', 'INC', 0.0, 205200),
        (2024, 5, 'Kozhikode', 142753, 140170, 98.19, 'MK Raghavan', 'INC', 0.0, 68229),
        (2024, 6, 'Malappuram', 196215, 180302, 91.88, 'ET Mohammed Basheer', 'IUML', 0.0, 150508),
        (2024, 7, 'Ponnani', 158634, 140568, 88.61, 'Abdussamad Samadani', 'IUML', 0.0, 120515),
        (2024, 8, 'Palakkad', 180543, 172439, 95.52, 'VK Sreekandan', 'INC', 0.0, 47439),
        (2024, 9, 'Alathur (SC)', 162487, 154230, 94.91, 'K. Radhakrishnan', 'CPI(M)', 0.0, 15947),
        (2024, 10, 'Thrissur', 171539, 154985, 90.37, 'Suresh Gopi', 'BJP', 0.0, 59880),
        (2024, 11, 'Chalakudy', 165824, 156239, 94.23, 'Benny Behanan', 'INC', 0.0, 26177),
        (2024, 12, 'Ernakulam', 172315, 161348, 93.63, 'Hibi Eden', 'INC', 0.0, 160869),
        (2024, 13, 'Idukki', 182543, 167935, 91.95, 'Dean Kuriakose', 'INC', 0.0, 100802),
        (2024, 14, 'Kottayam', 178394, 163892, 91.88, 'Francis George', 'INC', 0.0, 48121),
        (2024, 15, 'Alappuzha', 186748, 175439, 93.96, 'KC Venugopal', 'INC', 0.0, 45318),
        (2024, 16, 'Mavelikara (SC)', 175942, 161723, 91.92, 'Kodikunnil Suresh', 'INC', 0.0, 6302),
        (2024, 17, 'Pathanamthitta', 169852, 158432, 93.27, 'Anto Antony', 'INC', 0.0, 22669),
        (2024, 18, 'Kollam', 188643, 170345, 90.28, 'NK Premachandran', 'RSP', 0.0, 69416),
        (2024, 19, 'Attingal', 177423, 164892, 92.92, 'Adoor Prakash', 'INC', 0.0, 131),
        (2024, 20, 'Thiruvananthapuram', 191234, 176743, 92.41, 'Rajeev Chandrasekhar', 'BJP', 0.0, 10234) 
    ) AS actual_results(year, constituency_number, constituency_name, electors, total_votes, turnout_percentage, elected_member, elected_party, vote_share_percentage, margin)
WHERE
    election_results.year = actual_results.year
    AND election_results.constituency_number = actual_results.constituency_number;
