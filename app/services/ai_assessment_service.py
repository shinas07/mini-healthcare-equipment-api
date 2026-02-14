from app.repositories.enums import EquipmentStatus
from app.repositories.equipment import Equipment
from app.schemas.ai import AIAssessmentInput, AIAssessmentOutput


class AIAssessmentService:
    """Simulates AI security/risk assessment for equipment."""

    def generate(self, equipment: Equipment, payload: AIAssessmentInput) -> AIAssessmentOutput:
        score = 2
        risk_factors: list[str] = []
        recommendations: list[str] = [
            "Keep maintenance logs updated and review monthly",
            "Limit equipment access to authorized staff only",
            "Enable audit logging for operational changes",
        ]

        if equipment.status == EquipmentStatus.MAINTENANCE:
            score += 3
            risk_factors.append("Equipment is currently under maintenance")
        elif equipment.status == EquipmentStatus.IN_USE:
            score += 1
            risk_factors.append("Equipment is under continuous usage")
        elif equipment.status == EquipmentStatus.DECOMMISSIONED:
            score += 4
            risk_factors.append("Equipment is decommissioned and high risk")

        if payload.internet_connected:
            score += 2
            risk_factors.append("Network-connected equipment has expanded attack surface")
            recommendations.append("Segment this device on a restricted network")

        issue_count = len(payload.known_issues)
        if issue_count > 0:
            score += min(3, issue_count)
            risk_factors.append(f"{issue_count} known issue(s) reported")
            recommendations.append("Resolve known issues and re-assess risk")

        if payload.last_maintenance_days is not None and payload.last_maintenance_days > 180:
            score += 2
            risk_factors.append("Maintenance appears overdue")
            recommendations.append("Schedule preventive maintenance immediately")

        score = max(1, min(score, 10))

        if score >= 8:
            recommendations.append("Escalate this asset for urgent security review")
        elif score >= 5:
            recommendations.append("Plan remediation in the next maintenance cycle")

        if not risk_factors:
            risk_factors.append("No significant issues detected in provided input")

        return AIAssessmentOutput(
            risk_score=score,
            risk_factors=risk_factors,
            recommendations=recommendations,
        )
