# Detailed Data Verification Todo List

This list outlines the critical anomalies and patterns identified in the `report.md` that require manual verification or stakeholder clarification.

---

### 1. Target's Massive Apparel Market Share Surge
- [ ] **Context**: Target gained ~20-30 percentage points in Sportswear and Training Apparel, often reaching 40-50% share in the new version.
- **Related Questions**: [Question 5](#question-5-merchant-market-share-distribution-in-sportswear-original-delivery-scope), [Question 6](#question-6-merchant-market-share-distribution-in-training-original-delivery-scope), [Question 10](#question-10-merchant-market-share-in-sportswear-apparel-valid-l2-original-scope), [Question 11](#question-11-merchant-market-share-in-training-apparel-valid-l2-original-scope), [Question 12](#question-12-merchant-market-share-in-basketball-apparel-valid-l2-original-scope)
- **Reasoning**: This is the most significant redistribution in the report. Target went from a secondary player to the #1 market leader in these categories.
- **Verification Metric**: Check if the "new" version now captures Target's private labels (All in Motion, JoyLab) which might have been uncategorized or misattributed in the "old" version.
- **Hypothesis**: The old version used "Brand Attribution" (missing private labels), while the new version uses "Channel/Retailer Attribution."
- **Business Impact**: If this is a methodology change rather than market growth, YoY comparisons will be invalid without a backfill.

### 2. Dick's Sporting Goods Attribution Collapse
- [ ] **Context**: Dick's lost 13-22 percentage points across Basketball, Running, and Sportswear categories.
- **Related Questions**: [Question 4](#question-4-merchant-market-share-distribution-in-basketball-footwear-original-delivery-scope), [Question 5](#question-5-merchant-market-share-distribution-in-sportswear-original-delivery-scope), [Question 6](#question-6-merchant-market-share-distribution-in-training-original-delivery-scope), [Question 7](#question-7-merchant-market-share-distribution-in-running-original-delivery-scope), [Question 8](#question-8-merchant-market-share-distribution-in-basketball-original-delivery-scope), [Question 10](#question-10-merchant-market-share-in-sportswear-apparel-valid-l2-original-scope), [Question 11](#question-11-merchant-market-share-in-training-apparel-valid-l2-original-scope), [Question 12](#question-12-merchant-market-share-in-basketball-apparel-valid-l2-original-scope)
- **Reasoning**: In Running, Dick's dropped from 33.18% to 11.29%. This is too large to be organic market movement.
- **Verification Metric**: Audit if Nike, Hoka, and On products sold *at* Dick's are now being attributed to the brands directly (DTC) or to other buckets, leaving Dick's with only private-label data.
- **Hypothesis**: The new version has improved SKU-level routing, correctly moving brand-heavy sales out of the "General Sporting Goods" bucket.
- **Business Impact**: Dick's total market relevance may be severely underrepresented if third-party brand sales are excluded from their total.

### 3. Kohl's Uncharacteristic Basketball Dominance
- [ ] **Context**: Kohl's surged 21.13 points to become the #1 Basketball merchant (28.15% share), surpassing Nike.
- **Related Questions**: [Question 8](#question-8-merchant-market-share-distribution-in-basketball-original-delivery-scope), [Question 12](#question-12-merchant-market-share-in-basketball-apparel-valid-l2-original-scope)
- **Reasoning**: Kohl's is not traditionally a performance basketball destination. This result "fails the smell test."
- **Verification Metric**: Analyze the L3 categories and product descriptions within Kohl's Basketball bucket.
- **Hypothesis**: Casual graphic tees or NBA-licensed lifestyle apparel are being misclassified as "Performance Basketball" gear.
- **Business Impact**: Over-weighting lifestyle apparel as sports gear dilutes the technical category analysis.

### 4. Cheer/Dance Data Blackout Recovery
- [ ] **Context**: The old version showed 0% market share across all merchants for Cheer/Dance Apparel (valid L2), while the new version shows active markets for Kohl's and Target.
- **Related Questions**: [Question 2](#question-2-comparative-analysis-of-fop-taxonomy-and-row-distribution-old-vs.-new), [Question 14](#question-14-merchant-market-share-in-cheerdance-apparel-valid-l2-original-scope)
- **Reasoning**: Row counts for Cheer/Dance exploded by 81x (370 to 29,997 rows).
- **Verification Metric**: Confirm if the old version was dumping these records into "Other Apparel" or "Uncategorized."
- **Hypothesis**: A major taxonomy shift successfully mapped previous "orphan" records into the Cheer/Dance FOP.
- **Business Impact**: Excellent for new analysis, but prohibits any historical trend/YoY calculation for this category.

### 5. Category Perimeter Shrinkage (Basketball Footwear)
- [ ] **Context**: Total market GMV for Basketball Footwear decreased by 7.2% ($5.39B to $5.00B) despite the time and merchant scope being identical.
- **Related Questions**: [Question 3](#question-3-nike-market-share-analysis-in-basketball-footwear-original-delivery-scope)
- **Reasoning**: If the scope is the same, the pie shouldn't shrink unless items were removed from the category definition.
- **Verification Metric**: Identify which specific SKUs or sub-brands were present in the old "Basketball Footwear" but are missing in the new version.
- **Hypothesis**: The new version uses stricter classification criteria, excluding "basketball-inspired" casual sneakers that were previously included.
- **Business Impact**: Total market size metrics are not comparable between versions without a common taxonomy.

### 6. Specialty Brand Migration (Hoka & On)
- [ ] **Context**: On gained 6.18 points in Running, while specialty brands generally showed positive share diffs against general retailers.
- **Related Questions**: [Question 7](#question-7-merchant-market-share-distribution-in-running-original-delivery-scope), [Question 9](#question-9-merchant-market-share-distribution-in-hiking-original-delivery-scope)
- **Reasoning**: This aligns with known market trends (DTC growth), but the magnitude in the new data version is significantly higher.
- **Verification Metric**: Verify if DTC (Direct-to-Consumer) sales for these brands are being captured more aggressively in the "new" source.
- **Hypothesis**: The "new" source has better coverage of digital/DTC transaction streams for emerging specialty brands.
- **Business Impact**: Provides a more accurate view of the current competitive landscape but complicates "Specialty vs. Big Box" historical comparisons.

### 7. Merchant Scope Expansion Bias
- [ ] **Context**: 7 new merchants (Amazon Leia, Costco, Macy's, etc.) added, representing a 70% coverage expansion.
- **Related Questions**: [Question 1](#question-1-comparative-analysis-of-merchant-presence-across-data-versions-old-vs.-new)
- **Reasoning**: Total GMV and row counts are heavily skewed by these additions.
- **Verification Metric**: Ensure all YoY and Share calculations in the final report strictly use the "Original Delivery Scope" (10 common merchants) unless explicitly stated otherwise.
- **Hypothesis**: Simple aggregate comparisons will show "false growth" due to the broader data net.
- **Business Impact**: Critical for executive reporting—growth due to "better data" must be separated from "better sales."
