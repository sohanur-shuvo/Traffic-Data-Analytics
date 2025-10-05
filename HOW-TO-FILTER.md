# How to Filter by Ratio Threshold

## Quick Guide: Show Only 6x (or greater) and Zero Values

Follow these simple steps to filter your comparison table:

### Step 1: Set Your Threshold
1. Look at the **"Comparison Settings"** card
2. Find **"Minimum ratio for highlighting"** dropdown
3. Select **"6x or greater"** (or any threshold you want)

### Step 2: Enable Filtering
1. Check the box: **"Show only highlighted time slots"**
2. You should see a yellow badge appear: 🔍 Active Filter: Showing only rows with ≥6x ratio or zero values

### Step 3: View Filtered Results
The comparison table will now show ONLY:
- ✅ Rows where Customer In ratio is ≥6x
- ✅ Rows where Customer Out ratio is ≥6x  
- ✅ Rows with any zero values
- ❌ Everything else is hidden

## Understanding the Filter

### What Gets Shown?

**Example with 6x threshold:**

| Scenario | Date1 In | Date2 In | Ratio | Shown? |
|----------|----------|----------|-------|--------|
| High ratio | 10 | 65 | 6.5x | ✅ YES (≥6x) |
| Exact threshold | 10 | 60 | 6.0x | ✅ YES (≥6x) |
| Below threshold | 10 | 50 | 5.0x | ❌ NO (<6x) |
| Zero value | 0 | 50 | ∞ | ✅ YES (zero) |
| Zero value | 30 | 0 | ∞ | ✅ YES (zero) |
| Normal | 25 | 30 | 1.2x | ❌ NO (<6x) |

### Ratio Calculation

```
Ratio = max(value1, value2) / min(value1, value2)
```

This ensures the ratio is always ≥ 1.0 (or infinity if one value is zero).

**Examples:**
- 10 vs 60 → 60/10 = **6.0x**
- 60 vs 10 → 60/10 = **6.0x** (same result)
- 5 vs 35 → 35/5 = **7.0x**
- 20 vs 24 → 24/20 = **1.2x**

## Visual Indicators

### When Filter is ACTIVE:
1. **Yellow badge** in Comparison Settings: "🔍 Active Filter: Showing only rows with ≥6x ratio or zero values"
2. **Table description** shows: "(showing only ≥6x ratio or zero values)"
3. **Fewer rows** in the table (only those matching criteria)

### When Filter is OFF:
1. No yellow badge
2. Table shows: "with X time slots shown" (all 48 time slots)
3. All rows visible with highlighting

## Color Coding

Even without the filter, you can see highlighting:

| Color | Meaning |
|-------|---------|
| 🔴 Red | Zero values or highlighted difference columns |
| 🟠 Amber | Values exceeding the selected threshold |
| ⚫ Gray | Normal values below threshold |

## Common Use Cases

### Use Case 1: Find Major Changes
**Goal**: Find time slots with dramatic differences

**Steps:**
1. Set threshold: **6x or greater**
2. ✅ Check "Show only highlighted time slots"
3. Result: Only shows major spikes or drops

### Use Case 2: Find Data Issues
**Goal**: Find time slots with missing data (zeros)

**Steps:**
1. Set any threshold (doesn't matter)
2. ✅ Check "Show only highlighted time slots"
3. Look for 🔴 red cells
4. Result: Quickly spot zero values

### Use Case 3: Review Everything with Visual Cues
**Goal**: See all data but highlight important changes

**Steps:**
1. Set threshold: **6x or greater**
2. ❌ Uncheck "Show only highlighted time slots"
3. Result: See all 48 time slots with visual highlighting

### Use Case 4: Adjust Sensitivity
**Goal**: Find more or fewer highlighted rows

**Steps:**
1. Start with **6x or greater**
2. If too few results → Try **5x** or **4x**
3. If too many results → Try **7x** or **8x**
4. ✅ Keep "Show only highlighted" checked
5. Result: Dynamic filtering as you change threshold

## Troubleshooting

### "I changed threshold but nothing happened"
**Solution:** Make sure "Show only highlighted time slots" checkbox is checked.

### "I see all rows with highlighting"
**This is correct if:** The checkbox is unchecked. This shows all data with visual highlighting only.

### "No rows are shown"
**Possible reasons:**
- Threshold is too high (try 4x or 5x)
- No data has that high a ratio
- Try unchecking filter to see all data first

### "I see zero values even with high threshold"
**This is correct!** Zero values are ALWAYS shown when filter is active, regardless of threshold setting.

## Step-by-Step Example

Let's walk through a complete example:

### Starting State
- You have uploaded Excel data
- Selected Date1: 2024-01-01
- Selected Date2: 2024-01-02
- All 48 time slots visible

### Action 1: Set Threshold
- Change dropdown to **"6x or greater"**
- **Result**: Table still shows all rows, but now has amber highlighting on 6x+ values

### Action 2: Enable Filter
- ✅ Check "Show only highlighted time slots"
- **Result**: 
  - Yellow badge appears: "🔍 Active Filter..."
  - Table now shows only 12 rows (example)
  - Description: "(showing only ≥6x ratio or zero values)"

### Action 3: Adjust Threshold
- Change dropdown to **"8x or greater"**
- **Result**: 
  - Filter badge updates: "≥8x ratio or zero values"
  - Table now shows only 5 rows (fewer because threshold is higher)
  - Amber highlighting only appears on 8x+ values

### Action 4: Disable Filter
- ❌ Uncheck "Show only highlighted time slots"
- **Result**:
  - Badge disappears
  - All 48 rows shown again
  - 8x+ values still highlighted in amber/red

## API Details

When filter is enabled, here's what happens:

```javascript
// Frontend sends request
{
  "min_ratio_threshold": 6,
  "show_highlighted_only": true
}

// Backend calculates ratio for each row
ratio = max(value1, value2) / min(value1, value2)

// Backend marks rows for highlighting
if (value1 == 0 OR value2 == 0 OR ratio >= 6) {
  should_highlight = true
}

// Backend filters results if requested
if (show_highlighted_only) {
  return only rows where should_highlight == true
}
```

## Best Practices

1. **Start Broad**: Begin with 4x threshold to see more results
2. **Refine**: Increase threshold to focus on bigger changes
3. **Use Filter**: Enable "Show only highlighted" to reduce noise
4. **Check Zeros**: Always review zero values (data quality issues)
5. **Compare Thresholds**: Try different values to find patterns

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│ FILTER FEATURE QUICK REFERENCE              │
├─────────────────────────────────────────────┤
│                                             │
│ TO SEE ONLY 6x+ AND ZEROS:                  │
│ 1. Set threshold: 6x or greater             │
│ 2. ✅ Check "Show only highlighted"         │
│                                             │
│ TO SEE ALL DATA WITH HIGHLIGHTING:          │
│ 1. Set threshold: 6x or greater             │
│ 2. ❌ Uncheck "Show only highlighted"       │
│                                             │
│ COLORS:                                     │
│ 🔴 Red = Zero or highlighted difference     │
│ 🟠 Amber = Exceeds threshold                │
│ ⚫ Gray = Normal                             │
│                                             │
│ RATIO FORMULA:                              │
│ max(value1, value2) / min(value1, value2)   │
│                                             │
└─────────────────────────────────────────────┘
```

---

**Need Help?** 
- See `HIGHLIGHTING-FIX.md` for technical details
- See `QUICK-START.md` for setup instructions
- Check backend terminal for debugging output

