-- Question 2A
-- Count distinct Acacia species in the taxonomy table.

SELECT COUNT(DISTINCT species) AS acacia_species_count
FROM taxonomy
WHERE species LIKE 'Acacia%';


-- Question 2B
-- Find the wheat type associated with the longest genomic DNA sequence.

SELECT
    tx.species AS wheat_type,
    rs.length AS dna_sequence_length
FROM rfamseq AS rs
JOIN taxonomy AS tx
    ON tx.ncbi_id = rs.ncbi_id
WHERE tx.species LIKE '%wheat%'
  AND rs.mol_type = 'genomic DNA'
ORDER BY rs.length DESC
LIMIT 1;

-- Question 2C
-- Return page 9 (15 results per page) of families whose maximum
-- associated genomic DNA sequence length exceeds 1,000,000.

SELECT
    f.rfam_acc AS family_accession,
    f.rfam_id AS family_name,
    MAX(rs.length) AS max_dna_sequence_length
FROM family AS f
JOIN full_region AS fr
    ON fr.rfam_acc = f.rfam_acc
JOIN rfamseq AS rs
    ON rs.rfamseq_acc = fr.rfamseq_acc
WHERE rs.mol_type = 'genomic DNA'
GROUP BY
    f.rfam_acc,
    f.rfam_id
HAVING MAX(rs.length) > 1000000
ORDER BY max_dna_sequence_length DESC
LIMIT 15 OFFSET 120;