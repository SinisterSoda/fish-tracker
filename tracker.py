import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Now you can import your_script
import main  # Replace 'your_script' with the actual name of the file

if __name__ == "__main__":
    main.main()
