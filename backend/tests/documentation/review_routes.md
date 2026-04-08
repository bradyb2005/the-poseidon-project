Review Route Test Documentation

<img width="612" height="127" alt="Screenshot 2026-04-07 at 11 26 14 AM" src="https://github.com/user-attachments/assets/5f04f19f-4069-4704-8b3d-b94630247fdb" />

- The first test loads valid data using equivalence partitioning to ensure it is shown in ReviewDisplay
- The second test uses equivalence partitioninng and exception handling to load all data and handle a missing review file
- The third test uses fault injection and exception handling to load all corrupted review data to ensure it is handled correctly
- There is a serialization test to ensure the review display is serialized correctly
- The last test uses boundary value analysis to ensure the repository bound objects still comply with the 1-5 rule
