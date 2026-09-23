#!/usr/bin/env python
"""Weakness 2: the null is partly a test of 'no objects to relate'.

For the Selection -> Proposed comparison, report the effect and its minimum detectable
effect (MDE, 80% power, two-sided alpha = 0.05) in:
  * all items                         (what the abstract currently summarises)
  * items where the relation block was non-empty
  * items with at least one cross-tile relation
separately for relational and non-relational tasks.

MDE = (z_{0.975} + z_{0.80}) * SE, with SE the paired-bootstrap standard deviation of the
mean difference. It answers: "how large a true effect would this sample reliably detect?"
"""
import numpy as np

from common import (HELD_OUT, PREREGISTERED_RELATIONAL, SEED, N_BOOT, correct, fmt_p, load,
                    mcnemar, pct, pp, write_json, write_text)

Z = 1.959964 + 0.841621


def se_boot(d, rng):
    d = np.asarray(d, float)
    return float(d[rng.integers(0, d.size, (N_BOOT, d.size))].mean(1).std()) if d.size else float("nan")


def main():
    rng = np.random.default_rng(SEED)
    data, uids = load()
    P = data["proposed_ctsr"]
    task = {u: P[u]["task"] for u in uids}
    nrel = {u: (P[u].get("artifacts") or {}).get("n_relations_built") or 0 for u in uids}
    ncross = {u: ((P[u].get("artifacts") or {}).get("graph_stats") or {}).get("n_cross_tile") or 0
              for u in uids}
    strata = {"all items": lambda u: True,
              "relation block non-empty": lambda u: nrel[u] > 0,
              ">=1 cross-tile relation": lambda u: ncross[u] > 0}
    groups = {"relational": lambda u: task[u] in PREREGISTERED_RELATIONAL,
              "non-relational": lambda u: task[u] not in PREREGISTERED_RELATIONAL and task[u] not in HELD_OUT}
    rows = []
    for sname, sf in strata.items():
        for gname, gf in groups.items():
            us = [u for u in uids if sf(u) and gf(u)]
            a, b = correct(data, "b3_selected", us), correct(data, "proposed_ctsr", us)
            res = mcnemar(a, b, rng)
            se = se_boot(b - a, rng)
            res.update({"stratum": sname, "group": gname, "se": se, "mde80": Z * se,
                        "share_of_group": len(us) / max(1, sum(1 for u in uids if gf(u)))})
            rows.append(res)
    write_json("r02_null_power.json", rows)

    md = ["# A2. The relation-block null, by what the block contained", "",
          "Selection -> Proposed, paired. MDE = smallest true effect detectable with 80% power "
          "(two-sided alpha 0.05). p-values uncorrected; the strata are post-treatment and "
          "therefore descriptive.", "",
          "| Stratum | Group | n | share of group | Delta (pp) [95% CI] | p | MDE (pp) |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['stratum']} | {r['group']} | {r['n']} | {pct(r['share_of_group'], 0)}% | "
                  f"{pp(r['delta'])} [{pp(r['lo'])}, {pp(r['hi'])}] | {fmt_p(r['p'])} | "
                  f"{100 * r['mde80']:.1f} |")
    write_text("r02_null_power.md", "\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
