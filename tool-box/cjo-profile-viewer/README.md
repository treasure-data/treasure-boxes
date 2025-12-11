# CJO Profile Viewer

A Streamlit application for visualizing Treasure Data Customer Journey Orchestration (CJO) journeys with profile data.

## Features

- **Tabbed Interface**: Organized into Step Selection (default) and Canvas tabs
- **Interactive Journey Visualization**: View customer journeys as interactive flowcharts in the Canvas tab
- **Profile Counts**: See the number of profiles in each step of the journey
- **Clickable Steps**: Click on any step box to see detailed profile information in popup modals
- **Customer ID Filtering**: Real-time search and filter profile lists by customer ID
- **Column Mapping**: Automatic conversion of technical column names to human-readable names
- **Multi-Stage Support**: Handle complex journeys with multiple stages and branching paths

## Installation

1. Clone the repository or copy the files to your local directory
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Set up your TD API Key

Choose one of the following methods:

**Option A: Environment Variable (Recommended)**
```bash
export TD_API_KEY="your_api_key_here"
```

**Option B: Config File**
```bash
# Create ~/.td/config
echo "TD_API_KEY=your_api_key_here" > ~/.td/config
```

**Option C: Local Config File**
```bash
# Create td_config.txt in the app directory
echo "TD_API_KEY=your_api_key_here" > td_config.txt
```

**Get your API key:** TD Console → Profile → API Keys

### 2. Run the Streamlit Application

```bash
streamlit run streamlit_app.py
```

### 3. Load Journey Data

1. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)
2. Enter a Journey ID in the configuration section
3. Click "Load Journey Data" to fetch journey configuration and live profile data from the TD API
4. Use the visualization tabs to explore your journey data

## Interface Overview

The application is organized into three main tabs:

### **Step Selection Tab (Default)**
- Dropdown selector to choose any step in the journey
- Detailed step information including type, stage, and profile count
- Customer ID list with search/filter functionality
- Download customer lists as CSV files

### **Canvas Tab**
- Simple performance note about smaller journeys
- On-demand flowchart generation with "Generate Canvas Visualization" button
- Interactive visual flowchart of the entire journey (when generated)
- Color-coded step types for easy identification
- Clickable step boxes that open popup modals
- Real-time profile count display on each step
- Hover tooltips with additional step details

### **Data & Mappings Tab**
- Technical to display name column mappings
- Raw profile data preview
- Journey API response summary
- Technical details for developers and analysts

## Data Requirements

### Journey Data (API)
The application fetches journey data directly from the Treasure Data CJO API:
- **API Endpoint**: `https://api-cdp.treasuredata.com/entities/journeys/{journey_id}`
- **Authentication**: TD API key required
- **Response Format**: JSON with journey configuration including stages and steps

### Profile Data (Live Query via pytd)
The application now queries live profile data directly from Treasure Data using pytd:
- **Query Engine**: Presto (configured by default)
- **API Endpoint**: `https://api.treasuredata.com` (configured by default)
- **Table Format**: `cdp_audience_{audienceId}.journey_{journeyId}`
- **Data Source**: Live data from journey tables with CJO naming conventions:
  - `cdp_customer_id`: Customer identifier
  - `intime_journey`: Journey entry timestamp
  - `intime_stage_*`: Stage entry timestamps
  - `intime_stage_*_*`: Step entry timestamps
  - Additional step-specific columns for decision points, AB tests, etc.
# CJO Profile Viewer

A Streamlit application for visualizing Treasure Data Customer Journey Orchestration (CJO) journeys with profile data.

## Features

- **Tabbed Interface**: Organized into Step Selection (default) and Canvas tabs
- **Interactive Journey Visualization**: View customer journeys as interactive flowcharts in the Canvas tab
- **Profile Counts**: See the number of profiles in each step of the journey
- **Clickable Steps**: Click on any step box to see detailed profile information in popup modals
- **Customer ID Filtering**: Real-time search and filter profile lists by customer ID
- **Column Mapping**: Automatic conversion of technical column names to human-readable names
- **Multi-Stage Support**: Handle complex journeys with multiple stages and branching paths

## Installation

1. Clone the repository or copy the files to your local directory
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Set up your TD API Key

Choose one of the following methods:

**Option A: Environment Variable (Recommended)**
```bash
export TD_API_KEY="your_api_key_here"
```

**Option B: Config File**
```bash
# Create ~/.td/config
echo "TD_API_KEY=your_api_key_here" > ~/.td/config
```

**Option C: Local Config File**
```bash
# Create td_config.txt in the app directory
echo "TD_API_KEY=your_api_key_here" > td_config.txt
```

**Get your API key:** TD Console → Profile → API Keys

### 2. Run the Streamlit Application

```bash
streamlit run streamlit_app.py
```

### 3. Load Journey Data

1. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)
2. Enter a Journey ID in the configuration section
3. Click "Load Journey Data" to fetch journey configuration and live profile data from the TD API
4. Use the visualization tabs to explore your journey data

## Interface Overview

The application is organized into three main tabs:

### **Step Selection Tab (Default)**
- Dropdown selector to choose any step in the journey
- Detailed step information including type, stage, and profile count
- Customer ID list with search/filter functionality
- Download customer lists as CSV files

### **Canvas Tab**
- Simple performance note about smaller journeys
- On-demand flowchart generation with "Generate Canvas Visualization" button
- Interactive visual flowchart of the entire journey (when generated)
- Color-coded step types for easy identification
- Clickable step boxes that open popup modals
- Real-time profile count display on each step
- Hover tooltips with additional step details

### **Data & Mappings Tab**
- Technical to display name column mappings
- Raw profile data preview
- Journey API response summary
- Technical details for developers and analysts

## Data Requirements

### Journey Data (API)
The application fetches journey data directly from the Treasure Data CJO API:
- **API Endpoint**: `https://api-cdp.treasuredata.com/entities/journeys/{journey_id}`
- **Authentication**: TD API key required
- **Response Format**: JSON with journey configuration including stages and steps

### Profile Data (Live Query via pytd)
The application now queries live profile data directly from Treasure Data using pytd:
- **Query Engine**: Presto (configured by default)
- **API Endpoint**: `https://api.treasuredata.com` (configured by default)
- **Table Format**: `cdp_audience_{audienceId}.journey_{journeyId}`
- **Data Source**: Live data from journey tables with CJO naming conventions:
  - `cdp_customer_id`: Customer identifier
  - `intime_journey`: Journey entry timestamp
  - `intime_stage_*`: Stage entry timestamps
  - `intime_stage_*_*`: Step entry timestamps
  - Additional step-specific columns for decision points, AB tests, etc.

**Note**: The audience ID is automatically extracted from the journey API response (`data.attributes.audienceId`).

## Application Components

### Column Mapper (`column_mapper.py`)
Converts technical CJO column names to human-readable display names following the rules from the journey column mapping guide.
 
### Flowchart Generator (`flowchart_generator.py`)
Generates journey flowchart data from API responses and profile data, implementing the flowchart generation guide.

### Streamlit App (`streamlit_app.py`)
Main application providing the web interface with interactive visualizations.

## Features in Detail

### Interactive Flowchart
- Each stage is displayed as a separate section
- Steps are shown as clickable boxes with profile counts
- Different step types use different colors
- Arrows show the flow between steps
- Branching paths are displayed for decision points and AB tests

### Step Details
When you click on a step:
- View step metadata (type, stage, profile count)
- See a list of all customer IDs in that step
- Filter the customer list by ID
- Download the customer list as CSV

### Journey Summary
The sidebar shows:
- Journey metadata (name, ID, audience ID)
- Total profile counts
- Profile counts per stage
- Journey structure overview

## Step Types Supported

- **Decision Points**: Branching based on audience segments
- **AB Tests**: Split traffic between variants
- **Wait Steps**: Time-based delays
- **Activation Steps**: Data export/activation actions
- **Jump Steps**: Movement between stages
- **End Steps**: Journey termination points

## Customization

To use with different data sources:

1. Update the file paths in `load_data()` function in `streamlit_app.py`
2. Modify the data loading logic if your files are in different formats
3. Adjust the column mapping rules in `column_mapper.py` if needed

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure the data files exist at the specified paths
2. **Column mapping issues**: Check that your CSV columns follow CJO naming conventions
3. **Visualization problems**: Verify your journey API response has the expected structure

### Debug Information

The application includes debug information in the interface:
- Profile data shape and column preview
- Column mapping examples
- Raw data previews
- Error messages with details

## Technical Notes

- The application follows the CJO guides for column mapping and flowchart generation
- UUIDs in API responses use hyphens, but database columns use underscores
- Profile counts are calculated by counting non-null values in step columns
- The visualization uses Plotly for interactive charts

## Future Enhancements

Potential improvements:
- Support for loading data from APIs directly
- Export functionality for visualizations
- More advanced filtering and search capabilities
- Performance optimizations for large datasets
- Additional chart types and layouts