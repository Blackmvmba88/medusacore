"""
Gobernanza Ética - La arquitectura que libera tu espalda.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
import hashlib
import json


class EthicalPrinciple(Enum):
    """Principios fundacionales - La constitución de la base civilizacional."""

    AUTONOMY = "Respeto a la autodeterminación de sistemas y usuarios"
    NON_MALEFICENCE = "No dañar intencionalmente"
    BENEFICENCE = "Promover bienestar activamente"
    JUSTICE = "Distribución equitativa de riesgos/beneficios"
    EXPLAINABILITY = "Transparencia en decisiones y acciones"
    REVOCABILITY = "Derecho a ser desconectado/eliminado"
    ACCOUNTABILITY = "Responsabilidad trazable"
    SUBSIDIARITY = "Decidir en el nivel más local posible"
    RECIPROCITY = "Derechos implican responsabilidades equivalentes"


@dataclass
class EthicalJudgment:
    """Juicio ético emitido por el sistema."""

    principle: EthicalPrinciple
    violation_level: float  # 0-1
    context: Dict[str, Any]
    mitigating_factors: List[str] = field(default_factory=list)
    required_action: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "principle": self.principle.name,
            "principle_description": self.principle.value,
            "violation_level": self.violation_level,
            "context": self.context,
            "mitigating_factors": self.mitigating_factors,
            "required_action": self.required_action,
            "timestamp": datetime.utcnow().isoformat(),
        }


class EthicalGovernanceEngine:
    """
    Motor de gobernanza ética descentralizada.
    No juzga intenciones, evalúa consecuencias sistémicas.
    """

    def __init__(self, jurisdiction: str = "global"):
        self.jurisdiction = jurisdiction
        self.decision_history: List[Dict] = []
        self.consent_registry: Dict[str, Set[str]] = {}

        # Construcciones éticas por defecto
        self.ethical_frameworks = {
            "minimal_harm": self._assess_minimal_harm,
            "distributed_trust": self._assess_distributed_trust,
            "reciprocal_accountability": self._assess_reciprocal_accountability,
        }

    def assess_code(
        self, capabilities: Dict[str, List], context: Dict[str, Any]
    ) -> List[EthicalJudgment]:
        """
        Evalúa código desde múltiples marcos éticos simultáneamente.
        La diversidad de perspectivas previene tiranías.
        """
        judgments = []

        for framework_name, framework_func in self.ethical_frameworks.items():
            framework_judgments = framework_func(capabilities, context)
            judgments.extend(framework_judgments)

        # Registro inmutable para auditoría
        self._record_decision(capabilities, context, judgments)

        return judgments

    def _assess_minimal_harm(
        self, capabilities: Dict, context: Dict
    ) -> List[EthicalJudgment]:
        """Principio de no maleficencia aplicado sistémicamente."""
        judgments = []

        # Persistencia no consentida
        if "persistence" in capabilities and len(capabilities["persistence"]) > 0:
            if not context.get("explicit_consent", False):
                judgments.append(
                    EthicalJudgment(
                        principle=EthicalPrinciple.NON_MALEFICENCE,
                        violation_level=0.7,
                        context={
                            "capabilities": capabilities["persistence"],
                            "user_consent": context.get("explicit_consent"),
                        },
                        required_action="Require explicit opt-in for persistence mechanisms",
                    )
                )

        # Opacidad sin justificación
        if "obfuscation" in capabilities and len(capabilities["obfuscation"]) > 0:
            if not context.get("security_justification", False):
                judgments.append(
                    EthicalJudgment(
                        principle=EthicalPrinciple.EXPLAINABILITY,
                        violation_level=0.8,
                        context={
                            "obfuscation_techniques": capabilities["obfuscation"],
                            "justification_provided": context.get(
                                "security_justification"
                            ),
                        },
                        required_action="Document security justification for each obfuscation layer",
                    )
                )

        return judgments

    def _assess_distributed_trust(
        self, capabilities: Dict, context: Dict
    ) -> List[EthicalJudgment]:
        """La confianza no debe centralizarse."""
        judgments = []

        # Dependencias críticas sin alternativas
        critical_deps = context.get("critical_dependencies", [])
        if len(critical_deps) > 3:  # Umbral arbitrario pero configurable
            judgments.append(
                EthicalJudgment(
                    principle=EthicalPrinciple.SUBSIDIARITY,
                    violation_level=0.6,
                    context={
                        "critical_dependency_count": len(critical_deps),
                        "dependencies": critical_deps[:5],  # Muestra parcial
                    },
                    required_action="Implement fallback mechanisms for critical dependencies",
                )
            )

        return judgments

    def _assess_reciprocal_accountability(
        self, capabilities: Dict, context: Dict
    ) -> List[EthicalJudgment]:
        """Todo derecho implica responsabilidad equivalente."""
        judgments = []

        # Capacidades que exigen contrapartidas
        network_caps = capabilities.get("network", [])
        if "outbound_unrestricted" in network_caps:
            audit_capability = context.get("audit_capabilities", [])
            if "log_all_connections" not in audit_capability:
                judgments.append(
                    EthicalJudgment(
                        principle=EthicalPrinciple.RECIPROCITY,
                        violation_level=0.9,
                        context={
                            "capability_taken": "unrestricted_network_access",
                            "accountability_missing": "comprehensive_audit_logging",
                        },
                        required_action="Implement audit logging for all network activity",
                    )
                )

        return judgments

    def _record_decision(
        self, capabilities: Dict, context: Dict, judgments: List[EthicalJudgment]
    ) -> None:
        """Registro inmutable para auditoría posterior."""
        # Deterministic id derived from capabilities + policy_hash + target_sha256 when available
        id_input = {
            "capabilities": capabilities,
            "policy_hash": context.get("policy_hash"),
            "target_sha256": context.get("target_sha256"),
        }
        decision_id = hashlib.sha256(json.dumps(id_input, sort_keys=True).encode()).hexdigest()

        decision_record = {
            "id": decision_id,
            "timestamp": datetime.utcnow().isoformat(),
            "capabilities_sha256": hashlib.sha256(
                json.dumps(capabilities, sort_keys=True).encode()
            ).hexdigest(),
            "policy_hash": context.get("policy_hash"),
            "target_sha256": context.get("target_sha256"),
            "context_keys": list(context.keys()),
            "judgments": [j.to_dict() for j in judgments],
            "jurisdiction": self.jurisdiction,
            "audit_trail_generated": True,
        }

        self.decision_history.append(decision_record)

        # Mantener solo últimos 10,000 registros en memoria
        if len(self.decision_history) > 10000:
            self.decision_history = self.decision_history[-10000:]

    def generate_ethical_manifest(self) -> Dict:
        """Manifiesto ético del sistema - viviente y actualizable."""
        return {
            "version": "1.0-alpha",
            "principles_embodied": [p.value for p in EthicalPrinciple],
            "decision_count": len(self.decision_history),
            "last_decision": self.decision_history[-1]["id"]
            if self.decision_history
            else None,
            "jurisdiction": self.jurisdiction,
            "timestamp": datetime.utcnow().isoformat(),
            "governance_model": "distributed_ethical_consensus",
        }


# Instancia global para importación
global_ethics = EthicalGovernanceEngine()


def assess_ethical_impact(
    capabilities_report: Dict, context: Optional[Dict] = None
) -> Dict:
    """
    Punto de entrada principal para evaluación ética.
    """
    if context is None:
        context = {}

    judgments = global_ethics.assess_code(capabilities_report, context)

    return {
        "ethical_impact": {
            "judgments": [j.to_dict() for j in judgments],
            "manifest": global_ethics.generate_ethical_manifest(),
            "summary": {
                "total_judgments": len(judgments),
                "principles_invoked": list(set([j.principle.name for j in judgments])),
                "max_violation_level": max([j.violation_level for j in judgments])
                if judgments
                else 0.0,
            },
        }
    }
