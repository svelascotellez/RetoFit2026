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
                <p class="text-muted" style="margin-bottom: 12px; font-size: 0.85rem;">Meta diaria: $\ge 300$ kcal o $\ge 10,000$ pasos (mínimo 4 días exitosos/semana).</p>
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

            <!-- Tabla General de Concentrado -->
            <div class="card col-12">
                <h2 style="font-size: 1.35rem; margin-bottom: 8px;">Concentrado Físico y Financiero</h2>
                {table_content}
            </div>
        </section>
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
    </script>
</body>
</html>
"""
    return html
