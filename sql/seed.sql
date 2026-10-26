-- Usuário de teste: admin / admin123
INSERT INTO usuario (login, senha_hash)
VALUES ('admin', crypt('admin123', gen_salt('bf')))
ON CONFLICT (login) DO NOTHING;

INSERT INTO area (nome) VALUES
('Tecnologia'), ('Saúde'), ('Design'), ('Direito'), ('Engenharia')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO carreira (titulo, descricao, salario_medio, area_id) VALUES
('Desenvolvedor de Software', 'Cria sistemas e aplicativos.', 6500.00, 1),
('Analista de Dados', 'Transforma dados em decisões.', 5800.00, 1),
('Enfermeiro', 'Cuida de pacientes e apoia equipes de saúde.', 4200.00, 2),
('Designer de Produto', 'Projeta interfaces e experiências.', 5200.00, 3),
('Engenheiro Civil', 'Planeja e acompanha obras.', 7000.00, 5);
