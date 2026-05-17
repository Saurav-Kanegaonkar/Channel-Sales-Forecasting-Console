window.projectData = {
  scenarios: {
    base: {
      name: "Base plan",
      metrics: [["Channel growth", "12.4%"], ["Forecast variance", "8.7%"], ["Promo ROI", "2.9x"], ["Comp flags", "4"]],
      insights: ["Growth is healthy, but variance is concentrated in two distributor territories.", "Compensation flags overlap with territories carrying the largest forecast miss."],
      recs: ["Keep the base plan only if dealer west coverage improves.", "Review incentive exposure before finalizing the monthly forecast."]
    },
    promo: {
      name: "Promotion push",
      metrics: [["Channel growth", "15.8%"], ["Forecast variance", "11.2%"], ["Promo ROI", "2.4x"], ["Comp flags", "7"]],
      insights: ["A promotion push increases top-line growth but creates wider forecast variance.", "The upside is not evenly distributed across dealer territories."],
      recs: ["Limit promotion expansion to territories with coverage above threshold.", "Do not scale the push where compensation risk is already high."]
    },
    coverage: {
      name: "Territory rebalance",
      metrics: [["Channel growth", "13.9%"], ["Forecast variance", "5.1%"], ["Promo ROI", "3.1x"], ["Comp flags", "2"]],
      insights: ["Rebalancing coverage improves forecast quality without relying on deeper discounts.", "The scenario reduces compensation risk and keeps promotion ROI healthy."],
      recs: ["Use the rebalance scenario as the planning recommendation.", "Move sales coverage toward dealer west before increasing promotion spend."]
    }
  },
  territories: [
    ["Dealer East", "Growing", 88, "Promotion upside"],
    ["Dealer West", "At risk", 46, "Coverage gap"],
    ["Commercial B2B", "Stable", 71, "Territory balance"],
    ["Retail Dealer", "Stable", 64, "Monitor"]
  ]
};
