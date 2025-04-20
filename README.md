# PagerDuty TSE Script 🔧📊

A lightweight Python script designed to **bulk create services in PagerDuty** using data from a `.csv` file, ideal for technical support engineering and DevOps workflows.

## 📌 Features
- Reads service data from a CSV file
- Automatically creates services via the **PagerDuty REST API**
- Simplifies large-scale service setup for teams and incident response

## 🛠️ Requirements
- Python 3.x
- `requests` library
- PagerDuty API key and permissions

## 🚀 Usage
1. Clone the repo:
   ```bash
   git clone https://github.com/brady-halsten/pagerDuty_tse.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Prepare your CSV file with service details.

5. Run the script:
   ```bash
   python create_services.py
## 📂 Example CSV Format
    
    service_name,description,escalation_policy
    My Service,Monitors API traffic,ABC123

## 🤝 Contributing
- Contributions are welcome! Feel free to open issues or submit pull requests to improve functionality or add new features.
