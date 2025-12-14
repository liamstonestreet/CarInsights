import kagglehub

# Data source 1 (Cars Dataset 2025)
path = kagglehub.dataset_download("abdulmalik1518/cars-datasets-2025")
print("Path to dataset files:", path)

# Data source 2 (Cars Dataset US Sales)
path = kagglehub.dataset_download("juanmerinobermejo/us-sales-cars-dataset")
print("Path to dataset files:", path)

# Data source 3 (Safety Ratings Dataset)
# scroll to ratings
link = "https://www.nhtsa.gov/nhtsa-datasets-and-apis#ratings"

# Data source 4 (Recalls Dataset 2025)
# scroll to recall
link = "https://www.nhtsa.gov/nhtsa-datasets-and-apis#recalls"

