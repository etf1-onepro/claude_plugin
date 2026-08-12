from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PluginContentTests(unittest.TestCase):
    def test_exemplo_de_busca_usa_query(self) -> None:
        plano = (ROOT / "skills/onepro-plano/SKILL.md").read_text(encoding="utf-8")
        self.assertIn('onepro_buscar_ativos(query="bova"', plano)
        self.assertNotIn("onepro_buscar_ativos(termo=", plano)

    def test_readme_usa_namespace_da_skill(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/onepro:onepro-plano", readme)

    def test_plano_respeita_pedido_de_nao_executar_tool(self) -> None:
        plano = (ROOT / "skills/onepro-plano/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("não executar nenhuma tool", plano)
        self.assertIn("não leia resource nem chame o localizador", plano)

    def test_plano_distingue_janelas_moveis_de_multiperiodo(self) -> None:
        plano = (ROOT / "skills/onepro-plano/SKILL.md").read_text(encoding="utf-8")
        self.assertIn('ambos com `visao="janelas_moveis"`', plano)
        self.assertIn("Nunca entregue Multi Período", plano)

    def test_instalacao_distingue_os_clientes(self) -> None:
        conectar = (ROOT / "skills/onepro-conectar/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Gerenciar", conectar)
        sem_formatacao = conectar.replace("**", "")
        self.assertRegex(sem_formatacao, r"aba\s+Conectores")
        self.assertIn("entra junto com o plugin", conectar)
        self.assertNotIn("peça separada da instalação em todo cliente", conectar)

    def test_base_nominal_real_descreve_a_excecao_de_comportamento(self) -> None:
        lastro = (ROOT / "skills/analise-com-lastro/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertRegex(lastro, r"onepro_comportamento.*lado a lado")
        self.assertNotIn("Os demais motores devolvem **reais**", lastro)

    def test_frontmatter_tem_name_e_description(self) -> None:
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            texto = skill.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---\n", texto, re.DOTALL)
            self.assertIsNotNone(match, skill)
            cabecalho = match.group(1) if match else ""
            self.assertRegex(cabecalho, r"(?m)^name: \S+")
            self.assertRegex(cabecalho, r"(?m)^description: .+")


if __name__ == "__main__":
    unittest.main()
