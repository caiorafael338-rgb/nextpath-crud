-- Comandos SQL usados pelo sistema (app.py)

-- Login
SELECT id FROM usuario WHERE login = :login AND senha_hash = crypt(:senha, senha_hash);

-- Listar áreas
SELECT id, nome FROM area ORDER BY nome;

-- CREATE
INSERT INTO carreira (titulo, descricao, salario_medio, area_id) VALUES (:titulo, :descricao, :salario, :area_id);

-- READ com JOIN e filtros (área, texto no título e faixa salarial)
SELECT c.id, c.titulo, c.descricao, c.salario_medio, a.nome AS area
FROM carreira c
INNER JOIN area a ON a.id = c.area_id
WHERE (:area_id IS NULL OR c.area_id = :area_id)
  AND c.titulo ILIKE '%' || :texto || '%'
  AND c.salario_medio BETWEEN :min AND :max
ORDER BY c.titulo;

-- UPDATE
UPDATE carreira SET titulo=:titulo, descricao=:descricao, salario_medio=:salario, area_id=:area_id WHERE id=:id;

-- DELETE
DELETE FROM carreira WHERE id = :id;

-- Consulta agregada: carreiras por área
SELECT a.nome, COUNT(c.id) AS total, AVG(c.salario_medio) AS media
FROM area a LEFT JOIN carreira c ON c.area_id = a.id
GROUP BY a.nome ORDER BY a.nome;
