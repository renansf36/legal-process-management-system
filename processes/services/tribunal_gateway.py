from dataclasses import dataclass


@dataclass(frozen=True)
class TribunalProcessSnapshot:
    numero: str
    tribunal: str
    status_externo: str
    ultima_movimentacao: str


class TribunalGateway:
    """Interface inicial para futura integracao com APIs dos tribunais."""

    def buscar_processo(self, numero: str) -> TribunalProcessSnapshot:
        raise NotImplementedError


class MockTribunalGateway(TribunalGateway):
    def buscar_processo(self, numero: str) -> TribunalProcessSnapshot:
        return TribunalProcessSnapshot(
            numero=numero,
            tribunal="Mock TJ",
            status_externo="Em andamento",
            ultima_movimentacao="Movimentacao simulada para validacao interna.",
        )
