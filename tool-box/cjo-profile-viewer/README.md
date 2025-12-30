# CJO Profile Viewer

A Streamlit application for visualizing Treasure Data Customer Journey Orchestration (CJO) journeys with live profile data integration.

## 🎯 Overview

The CJO Profile Viewer provides comprehensive visualization of customer journeys from Treasure Data's CDP. It features real-time profile tracking, interactive canvas flowcharts, and detailed step information with live data integration.

## ✨ Key Features

- **🔄 Live Data Integration**: Real-time journey configuration and profile data from TD APIs
- **🎨 Interactive Canvas**: Horizontal flowchart visualization with clickable steps
- **📋 Step Selection**: Hierarchical dropdown with profile counts for precise navigation
- **🔍 Profile Viewing**: Customer ID filtering, search, and CSV export functionality
- **📊 Data Mapping**: Complete technical-to-display name mapping with full API response view
- **🎪 7 Step Types Supported**: Wait, Activation, Decision, AB Test, Jump, Merge, and End steps
- **📱 Responsive Design**: Clean interface that adapts to different screen sizes

## 🛠️ Installation

1. **Clone or download** the application files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### 1. Configure TD API Access

Choose one authentication method:

**Environment Variable (Recommended)**
```bash
export TD_API_KEY="your_api_key_here"
```

**Config File**
```bash
echo "TD_API_KEY=your_api_key_here" > ~/.td/config
```

**Local Config File**
```bash
echo "TD_API_KEY=your_api_key_here" > td_config.txt
```

**Get API Key**: TD Console → Profile → API Keys

### 2. Launch Application

```bash
streamlit run app.py
```

### 3. Load Journey Data

1. Open browser at `http://localhost:8501`
2. Enter a **Journey ID** in the configuration section
3. Click **"Load Journey Data"** - fetches configuration and live profile data
4. Explore using the three main tabs

## 📱 Interface Guide

### **📋 Step Selection Tab**
- **Hierarchical dropdown** with all journey steps (includes profile counts and UUIDs)
- **Detailed step info** shows step name, type, ID, and SQL query used
- **Customer ID list** with real-time search and filtering
- **CSV export** functionality for profile lists
- **Always shows step info** even for steps with 0 profiles

### **🎨 Canvas Tab**
- **Interactive flowchart** with horizontal stage layout (responsive)
- **Color-coded step types** for visual identification:
  - 🟨 Decision/AB Test/Merge (Yellow) - Branching logic
  - 🟪 Wait Steps (Pink/Red) - Time-based operations
  - 🟢 Activation (Green) - External actions
  - 🟦 Jump/End (Blue/Purple) - Navigation/completion
- **Clean display names** without UUIDs or duplicate profile counts
- **Hover tooltips** show "Step UUID: [shortened-id]"
- **Clickable steps** open profile detail modals
- **Single profile count** display per step (no duplication)

### **📊 Data & Mappings Tab**
- **Column mappings** (all technical → display name conversions)
- **Full API request/response** with redacted API key for transparency
- **No profile preview** or summary stats (focused on technical details)

## 🔧 Technical Architecture

### **Modular Design**
```
├── app.py                    # Main Streamlit application
├── src/
│   ├── services/
│   │   └── td_api.py        # TD API service layer
│   ├── components/
│   │   └── flowchart_renderer.py  # Canvas HTML generation
│   ├── styles/              # CSS styling (flowchart, modals, etc.)
│   ├── utils/               # Session state, profile filtering
│   ├── column_mapper.py     # Technical-to-display name mapping
│   ├── flowchart_generator.py     # Journey structure processing
│   └── hierarchical_step_formatter.py  # Dropdown formatting
├── docs/                    # Comprehensive guides
└── requirements.txt         # Dependencies
```

### **Data Sources**

**Journey Configuration**
- **API**: `https://api-cdp.treasuredata.com/entities/journeys/{journey_id}`
- **Authentication**: TD API key required
- **Response**: Complete journey structure with stages and steps

**Profile Data**
- **Source**: Live queries via pytd client to TD
- **Tables**: `cdp_audience_{audienceId}.journey_{journeyId}`
- **Columns**: CJO naming conventions (`cdp_customer_id`, `intime_stage_*`, etc.)
- **Engine**: Presto (default configuration)

## 🎪 Supported Step Types

| Type | Description | Visual Color |
|------|-------------|--------------|
| **Wait Steps** | Duration waits, condition waits | 🟪 Pink/Red |
| **Activation Steps** | Data exports, syndication | 🟢 Green |
| **Decision Points** | Segment-based branching | 🟨 Yellow/Beige |
| **AB Test Steps** | Split testing with variants | 🟨 Yellow/Beige |
| **Jump Steps** | Stage/journey transitions | 🟦 Blue/Purple |
| **Merge Steps** | Path consolidation | 🟨 Yellow/Beige |
| **End Steps** | Journey termination | 🟦 Blue/Purple |

## 🔍 Key Capabilities

### **Profile Tracking**
- **Real-time counts** for each step showing active profiles
- **SQL query display** showing exact logic used for profile filtering
- **Customer ID search** with instant filtering
- **CSV export** of customer lists per step

### **Hierarchy Display**
- **Clean step names** (no UUIDs in canvas, full detail in dropdown)
- **Proper indentation** for branching paths (Decision, AB Test, Wait Conditions)
- **Merge step handling** with consolidated post-merge paths
- **Breadcrumb context** for complex journey navigation

### **Canvas Features**
- **Horizontal stages** with responsive design (mobile-friendly fallback to vertical)
- **Clean tooltips** with shortened UUIDs for identification
- **No duplicate information** (single profile count, clean step names)
- **Interactive modals** with detailed profile information

## 📚 Documentation

For detailed technical information, see the `/docs` directory:

- **`PROJECT_SUMMARY.md`** - Complete technical overview and architecture
- **`STEP_TYPES_GUIDE.md`** - Implementation details for all 7 step types
- **`UI_IMPLEMENTATION_GUIDE.md`** - Interface patterns and formatting rules
- **`journey-tables-guide.md`** - Data structure and table schema reference

## 🚨 Troubleshooting

### **Common Issues**

**API Authentication**
- Verify TD API key is set correctly
- Check key has CDP access permissions

**Journey Loading**
- Ensure Journey ID exists and is accessible
- Verify journey has associated audience data

**Profile Data**
- Check that journey tables exist in TD
- Verify audience has profile data in the specified journey

**Performance**
- Use Step Selection tab for large journeys (better performance)
- Canvas generation is on-demand to avoid timeouts

### **Debug Information**

The application provides comprehensive debugging:
- **API request/response details** in Data & Mappings tab
- **SQL queries shown** for each step's profile filtering logic
- **Column mapping transparency** with full technical-to-display conversion
- **Error messages** with specific details for troubleshooting

## 🎯 Production Ready

This application is optimized for production use:
- **Modular architecture** for maintainability
- **Live data integration** with Treasure Data
- **Responsive design** for various screen sizes
- **Comprehensive documentation** for developers and users
- **Clean, minimal codebase** with zero development artifacts

Perfect for visualizing customer journey performance, debugging CJO configurations, and understanding customer flow patterns with real-time data from Treasure Data's Customer Data Platform.