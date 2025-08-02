### Flowchart Generator App (CSV Upload)

#### 🧩 Overview

This Flask application allows users to **upload a CSV file** that describes nodes and their levels. It automatically generates a **flowchart** based on the level relationships defined in the CSV.

------

#### ✅ Features

- Upload and parse CSV files
- Auto-generate node and edge relationships
- Sort nodes by level
- Render interactive flowchart (client side)
- Error handling for invalid file types or missing fields

------

#### 📂 Project Structure

```
csharpCopyEditproject/
├── app.py                # Main Flask application
├── templates/
│   ├── index.html        # Upload interface
│   └── flowchart.html    # Flowchart result page
├── uploads/              # Uploaded CSV files (temp storage)
├── static/               # Optional: styles/scripts (if any)
└── README.md             # This file
```

------

#### 📄 CSV File Format

Upload a `.csv` file with the following **3 columns**:

| Column Name | Description                               |
| ----------- | ----------------------------------------- |
| `key`       | The name/identifier of the node           |
| `from`      | Level number this node belongs to         |
| `to`        | Level number of its connected child nodes |



> Example row:
>
> ```
> nginx
> 
> 
> CopyEdit
> Login Page,2,3
> ```

------

#### 🧪 Sample CSV

```
csCopyEditkey,from,to
Landing Page,1,2
Signup Page,2,3
Login Page,2,3
User Dashboard,3,4
```

------

#### 🚀 Setup Instructions

1. **Clone the Repository**

   ```
   bashCopyEditgit clone https://github.com/your-username/flowchart-generator.git
   cd flowchart-generator
   ```

2. **Install Required Packages**
    Make sure Python 3.7+ is installed.

   ```
   bash
   
   
   CopyEdit
   pip install flask pandas
   ```

3. **Run the App**

   ```
   bash
   
   
   CopyEdit
   python app.py
   ```

4. **Open in Browser**
    Visit:

   ```
   cpp
   
   
   CopyEdit
   http://127.0.0.1:5000/
   ```

------

#### 🔐 File Upload Restrictions

- Only `.csv` files allowed
- Max file size: 16MB
- Uploads stored temporarily in the `uploads/` directory

------

#### 🛠 Built With

- Python 3.x
- Flask
- Pandas
- HTML, CSS, JavaScript

------

#### 📌 Notes

- The flowchart rendering (in `flowchart.html`) is expected to be handled with a frontend JS library like **D3.js** or **vis.js** (not included here unless implemented).
- Ensure your CSV has no missing headers or invalid levels.