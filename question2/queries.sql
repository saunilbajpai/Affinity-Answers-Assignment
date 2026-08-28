-- Question 2A
-- Count distinct Acacia species in the taxonomy table.

SELECT COUNT(DISTINCT species) AS acacia_species_count
FROM taxonomy
WHERE species LIKE 'Acacia%';
