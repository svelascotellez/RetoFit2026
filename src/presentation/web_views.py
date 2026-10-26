"""
Capa de Presentacion: Generador de Dashboard Web Interactivo (Dark Mode Energy Neon / Bento Grid)
Criterios EARS: AC-2.7, AC-2.9, WCAG 2.1 AA
"""
from src.application.challenge_service import ChallengeService


def render_dashboard_html(service: ChallengeService) -> str:
    """Genera la interfaz HTML5 / CSS3 / Vanilla JS del Dashboard Reto Fit 2026."""
    summary = service.get_general_summary()
    has_participants = summary.total_participants > 0

    # Construccion de filas de tabla o estado vacio
    if has_participants:
        participants_rows = ""
        for p in summary.participants:
            status_badge = (
                f'<span class="badge badge-success">{p.weeks_met} Semanas Cumplidas</span>'
                if p.weeks_met > 0
                else '<span class="badge badge-warning">Sin semanas cumplidas</span>'
            )
            net_class = "text-success" if p.net_balance >= p.total_contributed else "text-warning"
            participants_rows += f"""
            <tr>
                <td><strong>{p.name}</strong> <span class="text-muted">({p.participant_id})</span></td>
                <td><strong>${p.total_contributed:.2f}</strong> <span class="text-muted">/ $900.00</span></td>
                <td>{status_badge}</td>
                <td>{p.weeks_missed}</td>
                <td class="text-error">-${p.total_penalties:.2f}</td>
                <td class="text-success">+${p.total_earnings:.2f}</td>
                <td class="{net_class}"><strong>${p.net_balance:.2f}</strong></td>
                <td>
                    <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="quickPay('{p.participant_id}', 200)" title="Abonar $200 quincenales">+ $200</button>
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="quickPay('{p.participant_id}', 100)" title="Abonar $100 final">+ $100</button>
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="undoPayment('{p.participant_id}')" title="Anular último abono">↩️ Anular</button>
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;" onclick="editParticipant('{p.participant_id}', '{p.name}')" title="Editar nombre">✏️ Editar</button>
                        <button class="btn" style="padding: 4px 8px; font-size: 0.8rem; background: var(--error); color: white;" onclick="confirmDeleteParticipant('{p.participant_id}', '{p.name}')" title="Eliminar participante">🗑️</button>
                    </div>
                </td>
            </tr>
            """
        table_content = f"""
        <div class="table-responsive">
            <table class="data-table" aria-label="Concentrado de Participantes">
                <thead>
                    <tr>
                        <th scope="col">Participante</th>
                        <th scope="col">Aportado (Meta $900)</th>
                        <th scope="col">Semanas Cumplidas</th>
                        <th scope="col">Semanas Incumplidas</th>
                        <th scope="col">Penalizaciones</th>
                        <th scope="col">Ganancias Bolsa</th>
                        <th scope="col">Balance Neto Final</th>
                        <th scope="col">Gestión y Abonos</th>
                    </tr>
                </thead>
                <tbody>
                    {participants_rows}
                </tbody>
            </table>
        </div>
        """
    else:
        table_content = """
        <div class="empty-state" role="status" aria-live="polite">
            <div class="empty-icon" aria-hidden="true">🏃‍♂️</div>
            <h3>No hay participantes registrados</h3>
            <p>El Reto Fit aún no tiene miembros registrados. Utiliza el formulario de registro para agregar al primer participante de la DIDT.</p>
        </div>
        """

    # Construccion de la seccion de Informe Semanal (Semana 1 por defecto)
    if has_participants:
        report_w1 = service.get_weekly_report(1)
        weekly_rows = ""
        for wp in report_w1.participants:
            compliance_badge = (
                f'<span class="badge badge-success">{wp.successful_days}/7 días (Cumplió)</span>'
                if wp.is_met
                else f'<span class="badge badge-warning">{wp.successful_days}/7 días (Incumplió)</span>'
            )
            status_badge = (
                '<span class="badge badge-success">Al corriente</span>'
                if wp.financial_status == "AL_CORRIENTE"
                else f'<span class="badge badge-warning">Pendiente: -${wp.pending_amount:.2f}</span>'
            )
            penalty_str = f"-${wp.penalty:.2f}" if wp.penalty > 0 else "$0.00"
            penalty_class = "text-error" if wp.penalty > 0 else "text-muted"
            earnings_str = f"+${wp.earnings:.2f}" if wp.earnings > 0 else "$0.00"
            earnings_class = "text-success" if wp.earnings > 0 else "text-muted"
            impact_class = "text-success" if wp.net_balance_impact >= 0 else "text-error"

            weekly_rows += f"""
            <tr>
                <td><strong>{wp.name}</strong> <span class="text-muted">({wp.participant_id})</span></td>
                <td>{compliance_badge}</td>
                <td><strong>${wp.total_contributed:.2f}</strong> <span class="text-muted">/ ${wp.expected_contribution:.2f}</span></td>
                <td>{status_badge}</td>
                <td class="{penalty_class}">{penalty_str}</td>
                <td class="{earnings_class}">{earnings_str}</td>
                <td class="{impact_class}"><strong>${wp.net_balance_impact:+.2f}</strong></td>
            </tr>
            """

        status_closed_badge = (
            '<span class="badge badge-success" id="weekly-report-closed-badge">Semana Liquidada</span>'
            if report_w1.is_closed
            else '<span class="badge badge-warning" id="weekly-report-closed-badge">Semana en Curso / Preliminar</span>'
        )

        weekly_report_content = f"""
        <div id="weekly-report-kpis" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px;">
            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; padding: 16px;">
                <div class="metric-title">Tasa de Cumplimiento Físico</div>
                <div class="metric-value primary" id="kpi-compliance-rate">{report_w1.compliance_rate:.1f}%</div>
                <div class="text-muted" style="font-size: 0.85rem;" id="kpi-compliance-counts">{report_w1.met_count} cumplieron / {report_w1.missed_count} no cumplieron</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; padding: 16px;">
                <div class="metric-title">Cuota Exigible Acumulada</div>
                <div class="metric-value secondary" id="kpi-expected-quota">${report_w1.expected_contribution_per_participant:.2f}</div>
                <div class="text-muted" style="font-size: 0.85rem;" id="kpi-quota-status">{report_w1.participants_up_to_date} al corriente / {report_w1.participants_behind} pendientes</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; padding: 16px;">
                <div class="metric-title">Bolsa Semanal (Penalizaciones)</div>
                <div class="metric-value neon" id="kpi-pool-amount">${report_w1.pool_amount:.2f}</div>
                <div class="text-muted" style="font-size: 0.85rem;" id="kpi-gain-per-compliant">+${report_w1.gain_per_compliant:.2f} por cumplidor</div>
            </div>
        </div>
        <div class="table-responsive">
            <table class="data-table" aria-label="Informe Semanal de Cuotas y Cumplimiento">
                <thead>
                    <tr>
                        <th scope="col">Participante</th>
                        <th scope="col">Cumplimiento Físico (≥4 días)</th>
                        <th scope="col">Aportación Acumulada</th>
                        <th scope="col">Estatus de Cuota</th>
                        <th scope="col">Penalización</th>
                        <th scope="col">Ganancia Bolsa</th>
                        <th scope="col">Impacto Semanal</th>
                    </tr>
                </thead>
                <tbody id="weekly-report-table-body">
                    {weekly_rows}
                </tbody>
            </table>
        </div>
        """
    else:
        status_closed_badge = ""
        weekly_report_content = """
        <div id="weekly-report-empty" class="empty-state" role="status" aria-live="polite">
            <div class="empty-icon" aria-hidden="true">📊</div>
            <h3>Sin datos de informe semanal</h3>
            <p>No hay participantes registrados para generar el informe de la semana seleccionada.</p>
        </div>
        """

    # Construccion de la seccion de Estadisticas Integrales (FEAT-007)
    stats = service.get_global_statistics()
    has_activities = stats.total_activity_days > 0

    if has_activities:
        ranking_rows = ""
        for r in stats.ranking:
            if r.rank_position == 1:
                podium_badge = '<span class="badge badge-gold">🥇 1° Lugar (Oro)</span>'
            elif r.rank_position == 2:
                podium_badge = '<span class="badge badge-silver">🥈 2° Lugar (Plata)</span>'
            elif r.rank_position == 3:
                podium_badge = '<span class="badge badge-bronze">🥉 3° Lugar (Bronce)</span>'
            else:
                podium_badge = f'<span class="badge" style="background: rgba(255,255,255,0.05); color: var(--text-secondary);">{r.rank_position}°</span>'

            ranking_rows += f"""
            <tr>
                <td style="font-family: var(--font-mono); font-weight: 700;">#{r.rank_position}</td>
                <td><strong>{r.name}</strong> <span class="text-muted">({r.participant_id})</span></td>
                <td><span class="badge badge-success">{r.successful_days} días</span></td>
                <td style="font-family: var(--font-mono);">{r.total_calories:,.0f} kcal</td>
                <td style="font-family: var(--font-mono);">{r.total_steps:,}</td>
                <td>{podium_badge}</td>
            </tr>
            """

        trend_rows = ""
        for t in stats.weekly_trends:
            trend_rows += f"""
            <tr>
                <td style="font-weight: 700;">Semana {t.week_number}</td>
                <td><span class="badge badge-success">{t.successful_days} días</span></td>
                <td>{t.compliant_participants} / {t.total_participants}</td>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-family: var(--font-mono); font-weight: 600; min-width: 45px;">{t.compliance_rate:.1f}%</span>
                        <div class="trend-bar-container" style="flex: 1;">
                            <div class="trend-bar-fill" style="width: {min(100.0, max(0.0, t.compliance_rate))}%;"></div>
                        </div>
                    </div>
                </td>
                <td style="font-family: var(--font-mono); font-weight: 700;" class="text-success">${t.pool_amount:.2f}</td>
            </tr>
            """

        stats_tab_content = f"""
        <section class="bento-grid">
            <div class="card col-3">
                <div class="metric-title">🔥 Calorías Totales Quemadas</div>
                <div class="metric-value neon">{stats.total_calories:,.0f} <span style="font-size: 1rem; color: var(--text-secondary);">kcal</span></div>
                <p class="text-muted" style="margin-top: 8px;">Promedio diario: <strong class="text-primary">{stats.average_daily_calories:.1f} kcal/día</strong></p>
            </div>

            <div class="card col-3">
                <div class="metric-title">👟 Pasos Totales Caminados</div>
                <div class="metric-value primary">{stats.total_steps:,}</div>
                <p class="text-muted" style="margin-top: 8px;">Promedio diario: <strong class="text-primary">{stats.average_daily_steps:,.0f} pasos/día</strong></p>
            </div>

            <div class="card col-3">
                <div class="metric-title">⚡ Días Exitosos Registrados</div>
                <div class="metric-value secondary">{stats.total_successful_days} <span style="font-size: 1rem; color: var(--text-secondary);">/ {stats.total_activity_days} registros</span></div>
                <p class="text-muted" style="margin-top: 8px;">Efectividad colectiva: <strong class="text-success">{round((stats.total_successful_days / stats.total_activity_days * 100), 1) if stats.total_activity_days > 0 else 0.0}%</strong></p>
            </div>

            <div class="card col-3">
                <div class="metric-title">💰 Balance de Penalizaciones</div>
                <div class="metric-value text-error">-${stats.total_penalties:.2f}</div>
                <p class="text-muted" style="margin-top: 8px;">Bolsa distribuida: <strong class="text-success">+${stats.total_distributed_pool:.2f}</strong></p>
            </div>

            <div class="card col-7">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>
                        <h2 style="font-size: 1.35rem; margin-bottom: 4px;">🏆 Podio y Ranking de Rendimiento</h2>
                        <p class="text-muted" style="font-size: 0.85rem;">Ordenado por días exitosos acumulados (criterio de desempate por calorías quemadas).</p>
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="data-table" aria-label="Ranking de Participantes del Reto Fit">
                        <thead>
                            <tr>
                                <th scope="col">Pos</th>
                                <th scope="col">Participante</th>
                                <th scope="col">Días Exitosos</th>
                                <th scope="col">Calorías Totales</th>
                                <th scope="col">Pasos Totales</th>
                                <th scope="col">Podio</th>
                            </tr>
                        </thead>
                        <tbody>
                            {ranking_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card col-5">
                <div style="margin-bottom: 16px;">
                    <h2 style="font-size: 1.35rem; margin-bottom: 4px;">📈 Cumplimiento por Semana</h2>
                    <p class="text-muted" style="font-size: 0.85rem;">Evolución del reto a lo largo de las 9 semanas oficiales.</p>
                </div>
                <div class="table-responsive">
                    <table class="data-table" aria-label="Tendencias de Cumplimiento Semanal">
                        <thead>
                            <tr>
                                <th scope="col">Semana</th>
                                <th scope="col">Días Éxito</th>
                                <th scope="col">Cumplieron</th>
                                <th scope="col">Efectividad</th>
                                <th scope="col">Bolsa</th>
                            </tr>
                        </thead>
                        <tbody>
                            {trend_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
        """
    else:
        stats_tab_content = """
        <section class="bento-grid">
            <div class="card col-12">
                <div id="stats-empty-state" class="empty-state" role="status" aria-live="polite">
                    <div class="empty-icon" aria-hidden="true">📈</div>
                    <h3>No hay actividades registradas en el reto</h3>
                    <p>Aún no se han ingresado calorías ni pasos para los participantes. Registra actividades físicas diarias en el Panel General para activar la analítica integral y el podio de competición.</p>
                </div>
            </div>
        </section>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reto Fit 2026 - DIDT Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Fira+Code:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0F172A;
            --surface: #1E293B;
            --surface-hover: #27354A;
            --border: #334155;
            --primary: #10B981;
            --primary-hover: #059669;
            --secondary: #F97316;
            --secondary-hover: #EA580C;
            --neon-accent: #06B6D4;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --error: #EF4444;
            --font-family: 'Outfit', Inter, system-ui, sans-serif;
            --font-mono: 'Fira Code', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-primary);
            font-family: var(--font-family);
            line-height: 1.5;
            padding: 24px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}

        .logo-area h1 {{
            font-size: 2.25rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--neon-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .logo-area p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}

        .header-badge {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 9999px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* Bento Grid */
        .bento-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }}

        .card {{
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
        }}

        .col-4 {{ grid-column: span 4; }}
        .col-6 {{ grid-column: span 6; }}
        .col-8 {{ grid-column: span 8; }}
        .col-12 {{ grid-column: span 12; }}

        @media (max-width: 900px) {{
            .col-4, .col-6, .col-8 {{ grid-column: span 12; }}
        }}

        .metric-title {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }}

        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            font-family: var(--font-mono);
            color: var(--text-primary);
        }}

        .metric-value.primary {{ color: var(--primary); }}
        .metric-value.secondary {{ color: var(--secondary); }}
        .metric-value.neon {{ color: var(--neon-accent); }}

        /* Calendar schedule */
        .dates-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 12px;
        }}

        .date-item {{
            display: flex;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.03);
            padding: 10px 14px;
            border-radius: 8px;
            border-left: 3px solid var(--secondary);
            font-size: 0.9rem;
        }}

        .date-item span.amount {{
            font-family: var(--font-mono);
            color: var(--primary);
            font-weight: 600;
        }}

        /* Table */
        .table-responsive {{
            overflow-x: auto;
            margin-top: 16px;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }}

        .data-table th {{
            background: rgba(15, 23, 42, 0.6);
            color: var(--text-secondary);
            padding: 12px 16px;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }}

        .data-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
        }}

        .data-table tr:hover td {{
            background-color: var(--surface-hover);
        }}

        /* Badges */
        .badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .badge-success {{ background: rgba(16, 185, 129, 0.2); color: var(--primary); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.2); color: #F59E0B; }}

        .text-success {{ color: var(--primary); }}
        .text-warning {{ color: #F59E0B; }}
        .text-error {{ color: var(--error); }}
        .text-muted {{ color: var(--text-secondary); font-size: 0.85rem; }}

        /* Empty state */
        .empty-state {{
            text-align: center;
            padding: 48px 24px;
        }}

        .empty-icon {{
            font-size: 3rem;
            margin-bottom: 16px;
        }}

        .empty-state h3 {{
            font-size: 1.4rem;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}

        .empty-state p {{
            color: var(--text-secondary);
            max-width: 500px;
            margin: 0 auto;
        }}

        /* Interactive Forms in Cards */
        .action-form {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 16px;
        }}

        .form-row {{
            display: flex;
            gap: 12px;
        }}

        .form-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .form-label {{
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .form-input {{
            flex: 1;
            background: var(--bg-main);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 10px 14px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.95rem;
        }}

        .form-input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
        }}

        .btn {{
            background: var(--primary);
            color: #0F172A;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s ease;
        }}

        .btn:hover {{
            background: var(--primary-hover);
        }}

        .btn-secondary {{
            background: var(--secondary);
            color: #FFFFFF;
        }}

        .btn-secondary:hover {{
            background: var(--secondary-hover);
        }}

        /* Tabs Navigation (FEAT-007) */
        .tabs-header {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 4px;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-family: var(--font-family);
            font-size: 1.05rem;
            font-weight: 700;
            padding: 10px 20px;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            position: relative;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.03);
        }}

        .tab-btn:focus-visible {{
            outline: 2px solid var(--neon-accent);
            outline-offset: 2px;
        }}

        .tab-btn.active {{
            color: var(--primary);
        }}

        .tab-btn.active::after {{
            content: '';
            position: absolute;
            bottom: -6px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--neon-accent));
            border-radius: 3px 3px 0 0;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }}

        .tab-panel {{
            display: block;
        }}

        .tab-panel.hidden {{
            display: none !important;
        }}

        /* Podium Badges */
        .badge-gold {{
            background: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }}
        .badge-silver {{
            background: rgba(148, 163, 184, 0.2);
            color: #CBD5E1;
            border: 1px solid rgba(148, 163, 184, 0.4);
        }}
        .badge-bronze {{
            background: rgba(217, 119, 6, 0.2);
            color: #F97316;
            border: 1px solid rgba(217, 119, 6, 0.4);
        }}

        /* Trend Bars */
        .trend-bar-container {{
            background: rgba(15, 23, 42, 0.6);
            border-radius: 6px;
            overflow: hidden;
            height: 10px;
            width: 100%;
            margin-top: 6px;
        }}
        .trend-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--neon-accent));
            border-radius: 6px;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-area">
                <h1>Reto Fit 2026</h1>
                <p>Dirección de Informática y Desarrollo Tecnológico (DIDT) • 19 Oct al 20 Dic</p>
            </div>
            <div class="header-badge" role="status">
                <span>●</span> Sistema Operativo en Railway
            </div>
        </header>

        <!-- Barra de Navegación por Pestañas Accesible (AC-7.5) -->
        <nav class="tabs-header" role="tablist" aria-label="Navegación del Reto Fit">
            <button id="tab-general" class="tab-btn active" role="tab" aria-selected="true" aria-controls="panel-general" tabindex="0" onclick="switchTab('general')">
                <span>📋</span> Panel General
            </button>
            <button id="tab-stats" class="tab-btn" role="tab" aria-selected="false" aria-controls="panel-stats" tabindex="-1" onclick="switchTab('stats')">
                <span>📊</span> Estadísticas del Reto
            </button>
        </nav>

        <div id="panel-general" class="tab-panel" role="tabpanel" aria-labelledby="tab-general" tabindex="0">
        <section class="bento-grid">
            <!-- Metrica 1: Bolsa Semanal -->
            <div class="card col-4">
                <div class="metric-title">Bolsa Semanal / Rollover</div>
                <div class="metric-value neon">${summary.total_rollover_balance:.2f}</div>
                <p class="text-muted" style="margin-top: 8px;">Fondo acumulado de penalizaciones repartible entre cumplidores.</p>
            </div>

            <!-- Metrica 2: Participantes -->
            <div class="card col-4">
                <div class="metric-title">Miembros Registrados</div>
                <div class="metric-value primary">{summary.total_participants}</div>
                <p class="text-muted" style="margin-top: 8px;">Meta semanal: 4 días de 300 kcal o 10,000 pasos.</p>
            </div>

            <!-- Metrica 3: Total Recaudado -->
            <div class="card col-4">
                <div class="metric-title">Fondo Total Aportado</div>
                <div class="metric-value secondary">${summary.total_funds_collected:.2f}</div>
                <p class="text-muted" style="margin-top: 8px;">Meta total: 4 quincenas de $200 + 1 semana de $100 = $900 por miembro.</p>
            </div>

            <!-- Calendario de Pagos -->
            <div class="card col-4">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px;">Fechas de Aportación ($900.00)</h3>
                <ul class="dates-list">
                    <li class="date-item"><span>1. 19 de octubre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>2. 2 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>3. 16 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>4. 30 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>5. 14 de diciembre (1 sem)</span><span class="amount">$100.00</span></li>
                </ul>
            </div>

            <!-- Formulario 1: Inscribir Miembro -->
            <div class="card col-4">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px;">👤 Inscribir Miembro</h3>
                <p class="text-muted" style="margin-bottom: 12px; font-size: 0.85rem;">Registra un participante de la DIDT al reto.</p>
                <form class="action-form" onsubmit="event.preventDefault(); registerParticipant();">
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div class="form-group">
                            <label for="new-id" class="form-label">ID Único</label>
                            <input id="new-id" class="form-input" placeholder="Ej: didt-01" required>
                        </div>
                        <div class="form-group">
                            <label for="new-name" class="form-label">Nombre Completo</label>
                            <input id="new-name" class="form-input" placeholder="Nombre y apellido" required>
                        </div>
                        <button type="submit" class="btn" style="margin-top: 4px;">Inscribir Miembro</button>
                    </div>
                </form>
            </div>

            <!-- Formulario 2: Abonar Pago Quincenal -->
            <div class="card col-4">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px; color: var(--secondary);">💳 Abonar Pago Quincenal</h3>
                <p class="text-muted" style="margin-bottom: 12px; font-size: 0.85rem;">Cuota: 4 de $200 + 1 final de $100 ($900 en 5 fechas).</p>
                <form class="action-form" onsubmit="event.preventDefault(); submitPaymentForm();">
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div class="form-group">
                            <label for="pay-pid" class="form-label">ID de Miembro</label>
                            <input id="pay-pid" class="form-input" placeholder="Ej: didt-01" required>
                        </div>
                        <div class="form-group">
                            <label for="pay-amount" class="form-label">Monto a Abonar (MXN)</label>
                            <input id="pay-amount" type="number" step="0.01" class="form-input" placeholder="200.00" value="200.00" required>
                        </div>
                        <button type="submit" class="btn btn-secondary" style="margin-top: 4px;">💳 Abonar Pago Quincenal</button>
                    </div>
                </form>
            </div>

            <!-- Formulario 3: Registrar Actividad Diaria -->
            <div class="card col-8">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px;">🏃 Registrar Actividad Diaria</h3>
                <p class="text-muted" style="margin-bottom: 12px; font-size: 0.85rem;">Meta diaria: ≥ 300 kcal o ≥ 10,000 pasos (mínimo 4 días exitosos/semana).</p>
                <form class="action-form" onsubmit="event.preventDefault(); submitActivityForm();">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 12px; align-items: flex-end;">
                        <div class="form-group">
                            <label for="act-pid" class="form-label">ID Miembro</label>
                            <input id="act-pid" class="form-input" placeholder="Ej: didt-01" required>
                        </div>
                        <div class="form-group">
                            <label for="act-week" class="form-label">Semana</label>
                            <input id="act-week" type="number" min="1" max="9" class="form-input" placeholder="1-9" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="act-day" class="form-label">Día (1-7)</label>
                            <input id="act-day" type="number" min="1" max="7" class="form-input" placeholder="1-7" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="act-cals" class="form-label">Calorías</label>
                            <input id="act-cals" type="number" min="0" class="form-input" placeholder="≥ 300 kcal" value="350">
                        </div>
                        <div class="form-group">
                            <label for="act-steps" class="form-label">Pasos</label>
                            <input id="act-steps" type="number" min="0" class="form-input" placeholder="≥ 10,000" value="5000">
                        </div>
                        <div class="form-group" style="min-width: 140px; display: flex; gap: 6px;">
                            <button type="submit" class="btn" style="flex: 1; height: 42px;">Guardar</button>
                            <button type="button" class="btn btn-secondary" style="height: 42px;" onclick="clearDailyActivity()" title="Restablecer o limpiar el día">Limpiar</button>
                        </div>
                    </div>
                </form>
            </div>

            <!-- Formulario 4: Liquidar Semana -->
            <div class="card col-4">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px; color: var(--neon-accent);">⚖️ Liquidar Semana</h3>
                <p class="text-muted" style="margin-bottom: 12px; font-size: 0.85rem;">Penaliza $100 por incumplimiento y reparte la bolsa.</p>
                <form class="action-form" onsubmit="event.preventDefault(); submitCloseWeekForm();">
                    <div style="display: flex; gap: 8px; align-items: flex-end;">
                        <div class="form-group" style="flex: 1;">
                            <label for="close-week" class="form-label">Semana (1 a 9)</label>
                            <input id="close-week" type="number" min="1" max="9" class="form-input" placeholder="1-9" value="1" required>
                        </div>
                        <button type="submit" class="btn" style="background: var(--neon-accent); color: #0F172A; height: 42px;">Liquidar Semana</button>
                    </div>
                </form>
            </div>

            <!-- Seccion de Informe Semanal de Cuotas y Cumplimiento -->
            <div class="card col-12" id="weekly-report-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
                    <div>
                        <h2 style="font-size: 1.35rem; margin-bottom: 4px;">📊 Informe Semanal de Cuotas y Cumplimiento</h2>
                        <p class="text-muted" style="font-size: 0.85rem;">Auditoría de cuotas exigibles del calendario ($200 quincenales, $100 final) y cumplimiento físico semanal.</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        {status_closed_badge}
                        <label for="weekly-report-select" class="form-label" style="margin: 0; font-weight: 600;">Semana:</label>
                        <select id="weekly-report-select" class="form-input" style="width: auto; padding: 6px 14px; font-weight: 600; cursor: pointer;" onchange="loadWeeklyReport(this.value)">
                            <option value="1" selected>Semana 1 (19-25 oct)</option>
                            <option value="2">Semana 2 (26 oct - 1 nov)</option>
                            <option value="3">Semana 3 (2-8 nov)</option>
                            <option value="4">Semana 4 (9-15 nov)</option>
                            <option value="5">Semana 5 (16-22 nov)</option>
                            <option value="6">Semana 6 (23-29 nov)</option>
                            <option value="7">Semana 7 (30 nov - 6 dic)</option>
                            <option value="8">Semana 8 (7-13 dic)</option>
                            <option value="9">Semana 9 Final (14-20 dic)</option>
                        </select>
                    </div>
                </div>
                <div id="weekly-report-loading" style="display: none; padding: 24px; text-align: center; color: var(--neon-accent);" role="status" aria-live="polite">
                    ⏳ Cargando métricas e informe de la semana...
                </div>
                <div id="weekly-report-container">
                    {weekly_report_content}
                </div>
            </div>

            <!-- Tabla General de Concentrado -->
            <div class="card col-12">
                <h2 style="font-size: 1.35rem; margin-bottom: 8px;">Concentrado Físico y Financiero</h2>
                {table_content}
            </div>
        </section>
        </div>

        <!-- Panel de Estadísticas del Reto (AC-7.5, AC-7.6) -->
        <div id="panel-stats" class="tab-panel hidden" role="tabpanel" aria-labelledby="tab-stats" tabindex="0" style="display: none;">
            {stats_tab_content}
        </div>
    </div>

    <!-- Modal Accesible de Confirmacion -->
    <div id="confirmModal" role="dialog" aria-modal="true" aria-labelledby="confirmModalTitle" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.75); z-index:9999; align-items:center; justify-content:center;">
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:24px; max-width:440px; width:90%; box-shadow:0 10px 30px rgba(0,0,0,0.6);">
            <h3 id="confirmModalTitle" style="color:var(--error); margin-bottom:12px; font-size:1.2rem;">⚠️ Confirmar Eliminación</h3>
            <p id="confirmModalMessage" style="color:var(--text-secondary); margin-bottom:20px; font-size:0.95rem; line-height:1.5;"></p>
            <div style="display:flex; justify-content:flex-end; gap:10px;">
                <button id="cancelModalBtn" type="button" class="btn btn-secondary" onclick="closeConfirmModal()">Cancelar</button>
                <button id="confirmModalBtn" type="button" class="btn" style="background:var(--error); color:#fff;">Confirmar</button>
            </div>
        </div>
    </div>

    <!-- Toast Accesible de Notificaciones -->
    <div id="statusToast" role="status" aria-live="polite" style="display:none; position:fixed; bottom:20px; right:20px; background:var(--surface); border:1px solid var(--primary); padding:12px 20px; border-radius:8px; z-index:9998; color:var(--text-primary); box-shadow:0 4px 12px rgba(0,0,0,0.4);"></div>

    <script>
        let pendingAction = null;

        function showToast(message, isError = false) {{
            const toast = document.getElementById('statusToast');
            toast.textContent = message;
            toast.style.borderColor = isError ? 'var(--error)' : 'var(--primary)';
            toast.style.display = 'block';
            setTimeout(() => {{ toast.style.display = 'none'; }}, 3500);
        }}

        function openConfirmModal(message, onConfirm) {{
            const modal = document.getElementById('confirmModal');
            document.getElementById('confirmModalMessage').textContent = message;
            pendingAction = onConfirm;
            modal.style.display = 'flex';
            document.getElementById('confirmModalBtn').onclick = async () => {{
                if (pendingAction) await pendingAction();
                closeConfirmModal();
            }};
        }}

        function closeConfirmModal() {{
            document.getElementById('confirmModal').style.display = 'none';
            pendingAction = null;
        }}

        async function editParticipant(pid, currentName) {{
            const newName = prompt('Ingresa el nuevo nombre para el participante (' + pid + '):', currentName);
            if (newName === null) return;
            if (!newName.trim()) {{
                alert('El nombre no puede estar vacío.');
                return;
            }}
            const res = await fetch('/api/participants/' + encodeURIComponent(pid), {{
                method: 'PUT',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ name: newName.trim() }})
            }});
            if (res.ok) {{
                showToast('Nombre actualizado correctamente.');
                setTimeout(() => window.location.reload(), 600);
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al actualizar nombre');
            }}
        }}

        function confirmDeleteParticipant(pid, name) {{
            openConfirmModal(
                '¿Estás seguro de que deseas eliminar permanentemente a ' + name + ' (' + pid + ')? Se eliminarán también en cascada todos sus abonos y actividades.',
                async () => {{
                    const res = await fetch('/api/participants/' + encodeURIComponent(pid), {{
                        method: 'DELETE'
                    }});
                    if (res.ok) {{
                        showToast('Participante eliminado exitosamente.');
                        setTimeout(() => window.location.reload(), 600);
                    }} else {{
                        const err = await res.json();
                        alert(err.detail || 'Error al eliminar participante');
                    }}
                }}
            );
        }}

        async function undoPayment(pid) {{
            if (!confirm('¿Deseas anular la última aportación quincenal de ' + pid + '?')) return;
            const res = await fetch('/api/participants/' + encodeURIComponent(pid) + '/payments/last', {{
                method: 'DELETE'
            }});
            if (res.ok) {{
                const data = await res.json();
                alert('Abono anulado. Total acumulado actual: $' + data.total_contributed.toFixed(2));
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al anular abono');
            }}
        }}

        async function clearDailyActivity() {{
            const pid = document.getElementById('act-pid').value.trim();
            const weekStr = document.getElementById('act-week').value.trim();
            const dayStr = document.getElementById('act-day').value.trim();
            if (!pid || !weekStr || !dayStr) {{
                alert('Para limpiar un día, por favor ingresa el ID del miembro, la semana y el día.');
                return;
            }}
            if (!confirm('¿Limpiar y restablecer la actividad física del día ' + dayStr + ' en la semana ' + weekStr + ' para ' + pid + '?')) return;
            const res = await fetch('/api/activities/' + encodeURIComponent(pid) + '/weeks/' + encodeURIComponent(weekStr) + '/days/' + encodeURIComponent(dayStr), {{
                method: 'DELETE'
            }});
            if (res.ok) {{
                alert('Actividad eliminada y día restablecido.');
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al limpiar actividad');
            }}
        }}

        async function registerParticipant() {{
            const id = document.getElementById('new-id').value.trim();
            const name = document.getElementById('new-name').value.trim();
            if (!id || !name) return;
            const res = await fetch('/api/participants', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ id, name }})
            }});
            if (res.ok) {{
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al registrar miembro');
            }}
        }}

        async function quickPay(pid, amount) {{
            const res = await fetch('/api/payments', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ participant_id: pid, amount: amount }})
            }});
            if (res.ok) {{
                const data = await res.json();
                alert("¡Abono de $" + amount.toFixed(2) + " registrado para " + pid + "! Acumulado: $" + data.total_contributed.toFixed(2));
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al registrar abono');
            }}
        }}

        async function submitPaymentForm() {{
            const pid = document.getElementById('pay-pid').value.trim();
            const amtStr = document.getElementById('pay-amount').value.trim();
            if (!pid || !amtStr) return;
            const amount = parseFloat(amtStr);
            if (isNaN(amount) || amount <= 0) {{
                alert("Por favor ingresa un monto válido mayor a 0.");
                return;
            }}
            await quickPay(pid, amount);
        }}

        async function submitActivityForm() {{
            const pid = document.getElementById('act-pid').value.trim();
            const weekStr = document.getElementById('act-week').value.trim();
            const dayStr = document.getElementById('act-day').value.trim();
            const calStr = document.getElementById('act-cals').value.trim();
            const stepsStr = document.getElementById('act-steps').value.trim();
            if (!pid || !weekStr || !dayStr) return;

            const res = await fetch('/api/activity', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    participant_id: pid,
                    week_number: parseInt(weekStr),
                    day_of_week: parseInt(dayStr),
                    calories: parseInt(calStr || "0"),
                    steps: parseInt(stepsStr || "0")
                }})
            }});
            if (res.ok) {{
                const data = await res.json();
                const statusMsg = data.is_successful ? "¡DÍA EXITOSO! Cumple con la meta (>= 300 kcal o >= 10,000 pasos)." : "Día registrado (no alcanzó la meta diaria).";
                alert(statusMsg);
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al registrar actividad');
            }}
        }}

        async function submitCloseWeekForm() {{
            const weekStr = document.getElementById('close-week').value.trim();
            if (!weekStr) return;
            const res = await fetch('/api/weeks/' + encodeURIComponent(weekStr) + '/close', {{
                method: 'POST'
            }});
            if (res.ok) {{
                const data = await res.json();
                alert("¡Semana " + data.week_number + " liquidada! Cumplidores: " + data.met_count + " | Incumplidores: " + data.missed_count + " | Bolsa: $" + data.pool_collected + " | Ganancia por persona: $" + data.gain_per_participant);
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al liquidar la semana');
            }}
        }}

        async function loadWeeklyReport(week) {{
            const loading = document.getElementById('weekly-report-loading');
            const container = document.getElementById('weekly-report-container');
            if (loading) loading.style.display = 'block';
            if (container) container.style.opacity = '0.5';

            try {{
                const res = await fetch('/api/reports/weekly/' + encodeURIComponent(week));
                if (!res.ok) {{
                    const errData = await res.json();
                    throw new Error(errData.detail || 'Error al obtener informe semanal');
                }}
                const data = await res.json();
                renderWeeklyReportData(data);
            }} catch (err) {{
                showToast(err.message, true);
            }} finally {{
                if (loading) loading.style.display = 'none';
                if (container) container.style.opacity = '1';
            }}
        }}

        function renderWeeklyReportData(data) {{
            const closedBadge = document.getElementById('weekly-report-closed-badge');
            if (closedBadge) {{
                closedBadge.className = data.is_closed ? 'badge badge-success' : 'badge badge-warning';
                closedBadge.textContent = data.is_closed ? 'Semana Liquidada' : 'Semana en Curso / Preliminar';
            }}
            const rateEl = document.getElementById('kpi-compliance-rate');
            if (rateEl) rateEl.textContent = data.compliance_rate.toFixed(1) + '%';
            const countEl = document.getElementById('kpi-compliance-counts');
            if (countEl) countEl.textContent = data.met_count + ' cumplieron / ' + data.missed_count + ' no cumplieron';
            const quotaEl = document.getElementById('kpi-expected-quota');
            if (quotaEl) quotaEl.textContent = '$' + data.expected_contribution_per_participant.toFixed(2);
            const statusEl = document.getElementById('kpi-quota-status');
            if (statusEl) statusEl.textContent = data.participants_up_to_date + ' al corriente / ' + data.participants_behind + ' pendientes';
            const poolEl = document.getElementById('kpi-pool-amount');
            if (poolEl) poolEl.textContent = '$' + data.pool_amount.toFixed(2);
            const gainEl = document.getElementById('kpi-gain-per-compliant');
            if (gainEl) gainEl.textContent = '+$' + data.gain_per_compliant.toFixed(2) + ' por cumplidor';

            const tbody = document.getElementById('weekly-report-table-body');
            if (tbody && data.participants) {{
                tbody.innerHTML = data.participants.map(p => {{
                    const compBadge = p.is_met 
                        ? `<span class="badge badge-success">${{p.successful_days}}/7 días (Cumplió)</span>`
                        : `<span class="badge badge-warning">${{p.successful_days}}/7 días (Incumplió)</span>`;
                    const statusBadge = p.financial_status === 'AL_CORRIENTE'
                        ? `<span class="badge badge-success">Al corriente</span>`
                        : `<span class="badge badge-warning">Pendiente: -$${{p.pending_amount.toFixed(2)}}</span>`;
                    const penStr = p.penalty > 0 ? `-$${{p.penalty.toFixed(2)}}` : '$0.00';
                    const penCls = p.penalty > 0 ? 'text-error' : 'text-muted';
                    const earnStr = p.earnings > 0 ? `+$${{p.earnings.toFixed(2)}}` : '$0.00';
                    const earnCls = p.earnings > 0 ? 'text-success' : 'text-muted';
                    const impCls = p.net_balance_impact >= 0 ? 'text-success' : 'text-error';
                    const sign = p.net_balance_impact >= 0 ? '+' : '';

                    return `<tr>
                        <td><strong>${{p.name}}</strong> <span class="text-muted">(${{p.participant_id}})</span></td>
                        <td>${{compBadge}}</td>
                        <td><strong>$${{p.total_contributed.toFixed(2)}}</strong> <span class="text-muted">/ $${{p.expected_contribution.toFixed(2)}}</span></td>
                        <td>${{statusBadge}}</td>
                        <td class="${{penCls}}">${{penStr}}</td>
                        <td class="${{earnCls}}">${{earnStr}}</td>
                        <td class="${{impCls}}"><strong>${{sign}}$${{p.net_balance_impact.toFixed(2)}}</strong></td>
                    </tr>`;
                }}).join('');
            }}
        }}

        function switchTab(tabId) {{
            const tabGeneral = document.getElementById('tab-general');
            const tabStats = document.getElementById('tab-stats');
            const panelGeneral = document.getElementById('panel-general');
            const panelStats = document.getElementById('panel-stats');

            if (tabId === 'stats') {{
                if (tabGeneral) {{
                    tabGeneral.classList.remove('active');
                    tabGeneral.setAttribute('aria-selected', 'false');
                    tabGeneral.setAttribute('tabindex', '-1');
                }}
                if (tabStats) {{
                    tabStats.classList.add('active');
                    tabStats.setAttribute('aria-selected', 'true');
                    tabStats.setAttribute('tabindex', '0');
                }}
                if (panelGeneral) {{
                    panelGeneral.classList.add('hidden');
                    panelGeneral.style.display = 'none';
                }}
                if (panelStats) {{
                    panelStats.classList.remove('hidden');
                    panelStats.style.display = 'block';
                    panelStats.focus();
                }}
            }} else {{
                if (tabStats) {{
                    tabStats.classList.remove('active');
                    tabStats.setAttribute('aria-selected', 'false');
                    tabStats.setAttribute('tabindex', '-1');
                }}
                if (tabGeneral) {{
                    tabGeneral.classList.add('active');
                    tabGeneral.setAttribute('aria-selected', 'true');
                    tabGeneral.setAttribute('tabindex', '0');
                }}
                if (panelStats) {{
                    panelStats.classList.add('hidden');
                    panelStats.style.display = 'none';
                }}
                if (panelGeneral) {{
                    panelGeneral.classList.remove('hidden');
                    panelGeneral.style.display = 'block';
                    panelGeneral.focus();
                }}
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const tabs = [document.getElementById('tab-general'), document.getElementById('tab-stats')];
            tabs.forEach((tab, index) => {{
                if (!tab) return;
                tab.addEventListener('keydown', (e) => {{
                    let nextIndex = null;
                    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {{
                        nextIndex = (index + 1) % tabs.length;
                    }} else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {{
                        nextIndex = (index - 1 + tabs.length) % tabs.length;
                    }} else if (e.key === 'Home') {{
                        nextIndex = 0;
                    }} else if (e.key === 'End') {{
                        nextIndex = tabs.length - 1;
                    }}
                    if (nextIndex !== null) {{
                        e.preventDefault();
                        tabs[nextIndex].focus();
                        const tabTarget = nextIndex === 0 ? 'general' : 'stats';
                        switchTab(tabTarget);
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>
"""
    return html
