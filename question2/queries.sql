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