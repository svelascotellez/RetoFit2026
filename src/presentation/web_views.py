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
                <td>${p.total_contributed:.2f} / $1,000.00</td>
                <td>{status_badge}</td>
                <td>{p.weeks_missed}</td>
                <td class="text-error">-${p.total_penalties:.2f}</td>
                <td class="text-success">+${p.total_earnings:.2f}</td>
                <td class="{net_class}"><strong>${p.net_balance:.2f}</strong></td>
            </tr>
            """
        table_content = f"""
        <div class="table-responsive">
            <table class="data-table" aria-label="Concentrado de Participantes">
                <thead>
                    <tr>
                        <th scope="col">Participante</th>
                        <th scope="col">Aportado (Meta $1,000)</th>
                        <th scope="col">Semanas Cumplidas</th>
                        <th scope="col">Semanas Incumplidas</th>
                        <th scope="col">Penalizaciones</th>
                        <th scope="col">Ganancias Bolsa</th>
                        <th scope="col">Balance Neto Final</th>
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
                <p class="text-muted" style="margin-top: 8px;">Meta total: 5 quincenas de $200 = $1,000 por miembro.</p>
            </div>

            <!-- Calendario de Pagos -->
            <div class="card col-4">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px;">Fechas de Aportación ($1,000)</h3>
                <ul class="dates-list">
                    <li class="date-item"><span>1. 19 de octubre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>2. 2 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>3. 16 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>4. 30 de noviembre</span><span class="amount">$200.00</span></li>
                    <li class="date-item"><span>5. 14 de diciembre</span><span class="amount">$200.00</span></li>
                </ul>
            </div>

            <!-- Registro Rapido -->
            <div class="card col-8">
                <h3 style="font-size: 1.1rem; margin-bottom: 8px;">Acciones Rápidas del Reto</h3>
                <form class="action-form" onsubmit="event.preventDefault(); registerParticipant();">
                    <div class="form-row">
                        <input id="new-id" class="form-input" placeholder="ID (ej: p1)" required>
                        <input id="new-name" class="form-input" placeholder="Nombre completo" required>
                        <button type="submit" class="btn">Inscribir Miembro</button>
                    </div>
                </form>
                <div style="margin-top: 16px; display: flex; gap: 12px;">
                    <button class="btn btn-secondary" onclick="recordSampleActivity()">+ Cargar Día Exitoso (Ejemplo)</button>
                </div>
            </div>

            <!-- Tabla General de Concentrado -->
            <div class="card col-12">
                <h2 style="font-size: 1.35rem; margin-bottom: 8px;">Concentrado Físico y Financiero</h2>
                {table_content}
            </div>
        </section>
    </div>

    <script>
        async function registerParticipant() {{
            const id = document.getElementById('new-id').value;
            const name = document.getElementById('new-name').value;
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
                alert(err.detail || 'Error al registrar');
            }}
        }}

        async function recordSampleActivity() {{
            const pid = prompt("Ingresa el ID del participante:");
            if (!pid) return;
            const res = await fetch('/api/activity', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    participant_id: pid,
                    week_number: 1,
                    day_of_week: 1,
                    calories: 350,
                    steps: 5000
                }})
            }});
            if (res.ok) {{
                alert("¡Actividad registrada exitosamente como Día Exitoso (350 kcal)!");
                window.location.reload();
            }} else {{
                const err = await res.json();
                alert(err.detail || 'Error al registrar actividad');
            }}
        }}
    </script>
</body>
</html>
"""
    return html
