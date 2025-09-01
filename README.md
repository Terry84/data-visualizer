🥗 Data Visualizer – SDG Goal 2: Zero Hunger

This project is a data tool for creatives that helps analyze and visualize datasets related to UN Sustainable Development Goal 2 (Zero Hunger).
It enables users to upload data, explore patterns, and create shareable visualizations that highlight issues around food security, malnutrition, and sustainable agriculture.

🚀 Features

Upload datasets (CSV format)

Explore data (summary stats + raw preview)

Create visualizations (bar, line, scatter charts)

Custom themes and templates for creatives

Export & share visualizations (planned)

📖 About SDG Goal 2

“End hunger, achieve food security and improved nutrition, and promote sustainable agriculture.” – United Nations

This tool helps journalists, designers, researchers, and creatives tell compelling stories with data to advocate for Zero Hunger.

🛠️ Installation

Clone the repository:

git clone https://github.com/Terry84/data-visualizer.git
cd data-visualizer


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the app with:

streamlit run app.py


Then open your browser at http://localhost:5000
.

📊 Example Dataset

You can upload any CSV with columns like:

Country

Year

Malnutrition_Rate

Crop_Yield

Food_Production_Index

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License
