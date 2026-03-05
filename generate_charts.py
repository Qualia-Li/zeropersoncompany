#!/usr/bin/env python3
"""Generate charts for Zero Person Company book."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Style settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': '#cccccc',
})

COLORS = ['#2563eb', '#7c3aed', '#dc2626', '#059669', '#d97706', '#0891b2']
OUTPUT_DIR = 'assets/images'


def chart1_ai_investment():
    """Global AI Investment Growth (2018-2025)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025\n(forecast)']
    # Private AI investment in billions USD (Stanford AI Index, Goldman Sachs)
    investment = [40.4, 48.0, 67.9, 93.5, 91.9, 96.0, 252.3, 320.0]

    bars = ax.bar(years, investment, color=COLORS[0], width=0.6, edgecolor='white', linewidth=0.5)

    # Add value labels on top of bars with enough spacing
    for bar, val in zip(bars, investment):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
                f'${val:.0f}B', ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax.set_ylabel('Investment (Billion USD)', fontsize=12)
    ax.set_title('Global Private AI Investment Growth (2018-2025)', fontsize=14, pad=15)
    ax.set_ylim(0, 400)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-1-ai-investment.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 1: AI Investment - done")


def chart2_revenue_per_employee():
    """Revenue per Employee: AI-native vs Traditional Tech"""
    fig, ax = plt.subplots(figsize=(10, 6))

    companies = ['Copilot', 'NVIDIA', 'Netflix', 'OpenAI', 'Meta', 'Google', 'Apple', 'Microsoft', 'Traditional\nSaaS Avg']
    revenue = [4.2, 4.4, 4.15, 2.87, 1.85, 1.75, 2.4, 0.95, 0.35]
    colors = [COLORS[1] if r > 2.5 else COLORS[0] for r in revenue]

    bars = ax.barh(companies, revenue, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, revenue):
        ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height()/2,
                f'${val:.2f}M', ha='left', va='center', fontweight='bold', fontsize=10)

    ax.set_xlabel('Revenue per Employee (Million USD)', fontsize=12)
    ax.set_title('Revenue per Employee: AI-Native vs. Traditional Tech (2025)', fontsize=14, pad=15)
    ax.set_xlim(0, 5.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS[1], label='AI-Native / High Automation'),
                       Patch(facecolor=COLORS[0], label='Traditional Tech')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-2-revenue-per-employee.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 2: Revenue per Employee - done")


def chart3_company_evolution():
    """The Evolution: From Corporation to Zero-Person Company"""
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ['Traditional\nCorporation\n(2000s)', 'Lean Startup\n(2010s)', 'Solopreneur\n+ AI\n(2023-24)', 'One-Person\nUnicorn\n(2025-26)', 'Zero-Person\nCompany\n(2026+)']
    employees = [500, 50, 1, 1, 0]
    revenue_potential = [50, 10, 1, 100, 100]  # in millions

    x = np.arange(len(categories))

    # Plot employees as bars
    bars = ax.bar(x, [500, 50, 5, 1, 0.3], color=COLORS[2], width=0.4, label='Typical Employees', alpha=0.8)

    # Revenue potential on secondary axis
    ax2 = ax.twinx()
    ax2.plot(x, revenue_potential, color=COLORS[4], marker='D', linewidth=2.5, markersize=10, label='Revenue Potential ($M)')

    for i, (emp, rev) in enumerate(zip([500, 50, 5, 1, 0.3], revenue_potential)):
        if emp >= 1:
            ax.text(i, emp + 15, f'{int(emp)}', ha='center', va='bottom', fontweight='bold', fontsize=10, color=COLORS[2])
        else:
            ax.text(i, emp + 15, '0', ha='center', va='bottom', fontweight='bold', fontsize=10, color=COLORS[2])
        ax2.text(i, rev + 5, f'${rev}M', ha='center', va='bottom', fontweight='bold', fontsize=10, color=COLORS[4])

    ax.set_ylabel('Number of Employees', fontsize=12, color=COLORS[2])
    ax2.set_ylabel('Revenue Potential (Million USD)', fontsize=12, color=COLORS[4])
    ax.set_title('The Evolution: From Corporation to Zero-Person Company', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 600)
    ax2.set_ylim(0, 130)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=10)

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-3-company-evolution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 3: Company Evolution - done")


def chart4_agentic_ai_market():
    """AI Agent Market Size Growth"""
    fig, ax = plt.subplots(figsize=(10, 6))

    years = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    # AI Agent market size in billions (Grand View Research, MarketsandMarkets)
    market_size = [3.0, 5.2, 7.6, 12.0, 19.0, 28.0, 40.0, 52.6]

    ax.fill_between(range(len(years)), market_size, alpha=0.2, color=COLORS[1])
    ax.plot(range(len(years)), market_size, color=COLORS[1], marker='o', linewidth=2.5, markersize=8)

    for i, (y, val) in enumerate(zip(years, market_size)):
        offset = 3 if i % 2 == 0 else -4
        va = 'bottom' if offset > 0 else 'top'
        ax.text(i, val + offset, f'${val:.1f}B', ha='center', va=va, fontweight='bold', fontsize=10)

    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)
    ax.set_ylabel('Market Size (Billion USD)', fontsize=12)
    ax.set_title('AI Agent Market Size Growth (2023-2030)', fontsize=14, pad=15)
    ax.set_ylim(0, 65)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add CAGR annotation
    ax.annotate('CAGR: ~46%', xy=(5, 28), fontsize=13, fontweight='bold',
                color=COLORS[1], ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS[1], alpha=0.8))

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-4-ai-agent-market.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 4: AI Agent Market - done")


def chart5_freelancer_growth():
    """Solopreneur and Freelancer Growth"""
    fig, ax = plt.subplots(figsize=(10, 6))

    years = ['2020', '2021', '2022', '2023', '2024', '2025\n(est.)', '2027\n(proj.)']
    us_freelancers = [36, 40, 48, 56, 64, 70, 86.5]  # millions

    ax.fill_between(range(len(years)), us_freelancers, alpha=0.15, color=COLORS[3])
    ax.plot(range(len(years)), us_freelancers, color=COLORS[3], marker='s', linewidth=2.5, markersize=8)

    for i, val in enumerate(us_freelancers):
        offset = 3 if i % 2 == 0 else -4
        va = 'bottom' if offset > 0 else 'top'
        ax.text(i, val + offset, f'{val}M', ha='center', va=va, fontweight='bold', fontsize=10)

    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)
    ax.set_ylabel('U.S. Freelancers (Millions)', fontsize=12)
    ax.set_title('U.S. Freelancer & Solopreneur Growth (2020-2027)', fontsize=14, pad=15)
    ax.set_ylim(25, 100)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add annotation
    ax.annotate('+140% growth\n(2020→2027)', xy=(4.5, 55), fontsize=12, fontweight='bold',
                color=COLORS[3],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS[3], alpha=0.8))

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-5-freelancer-growth.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 5: Freelancer Growth - done")


def chart6_jobs_at_risk():
    """Jobs Most at Risk from AI Automation"""
    fig, ax = plt.subplots(figsize=(10, 6))

    jobs = [
        'Data Entry Clerks',
        'Customer Service Reps',
        'Bookkeepers/Accountants',
        'Administrative Assistants',
        'Content Writers',
        'Translators',
        'Graphic Designers',
        'Software Developers',
        'Marketing Analysts',
        'Legal Assistants'
    ]
    risk_pct = [95, 85, 80, 78, 72, 70, 65, 55, 52, 48]

    colors_gradient = plt.cm.RdYlGn_r(np.linspace(0.15, 0.85, len(jobs)))

    bars = ax.barh(jobs, risk_pct, color=colors_gradient, height=0.6, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, risk_pct):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', ha='left', va='center', fontweight='bold', fontsize=10)

    ax.set_xlabel('Automation Risk (%)', fontsize=12)
    ax.set_title('Jobs Most Susceptible to AI Automation (2025-2030)', fontsize=14, pad=15)
    ax.set_xlim(0, 110)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/figure-6-jobs-at-risk.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Chart 6: Jobs at Risk - done")


if __name__ == '__main__':
    chart1_ai_investment()
    chart2_revenue_per_employee()
    chart3_company_evolution()
    chart4_agentic_ai_market()
    chart5_freelancer_growth()
    chart6_jobs_at_risk()
    print("\nAll charts generated successfully!")
