# AI Evaluation Internship Report

## Introduction
This report presents the evaluation of two AI models, Tiny StarCoder and CodeLlama (7B-HF), on two distinct Python codebases. The purpose of this evaluation is to assess the models' capability to understand and generate code for an NP-hard problem-solving algorithm and a UDP socket-based server. 

## Dataset Description
To create dataset was used Python file **`divide.py`** with other python file as input.
Two Python files were used as datasets:
- **`file.py`** – A brute-force algorithm designed to solve an NP-hard problem.
- **`simple_file.py`** – A UDP socket-based server implementation.

### Dataset Structure
The dataset consists of:
- All previous lines as prefix.
- The first few characters of the new line as a prefix.
- A few lines of middle content.
- A few lines as a suffix.

## Model Performance Comparison
The evaluation was performed using the ChrF metric (Character n-gram F-score) to assess the similarity between the generated code and the reference implementation. Exact match was also tracked but remained 0 across all cases, which is expected due to minor syntactic variations such as different print formatting techniques (e.g., standard `print()` vs. f-strings) for this very reason I don't think exact match is reliable for LLM.

### Algorithm Code (`file.py`):
- **Tiny StarCoder:** ChrF = 28.39
- **CodeLlama:** ChrF = 82.03

### UDP Server Code (`simple_file.py`):
- **Tiny StarCoder:** ChrF = 0.0
- **CodeLlama:** ChrF = 38.43

## Interpretation of Results
The ChrF scores indicate that both models demonstrated some level of understanding of the algorithmic code. CodeLlama significantly outperformed Tiny StarCoder in this category, suggesting it was able to capture the structure and logic more effectively.

However, in the UDP server implementation, Tiny StarCoder failed to generate meaningful code (ChrF = 0.0), while CodeLlama achieved a moderate score (ChrF = 38.43). This disparity suggests that Tiny StarCoder struggled with socket-based networking concepts, whereas CodeLlama showed a partial but flawed grasp of the implementation.

Interestingly, despite the lack of exact matches, qualitative analysis of the generated code suggests that the models exhibited an emerging conceptual understanding. For instance, in the algorithmic code, the reference implementation utilized an `enum` to track directions, while CodeLlama instead generated a class-based `Enum` with different order (e.g., `P (right) and G (up)` vs. `L (left) and D (down)`). Similarly, in some cases, it replaced names (`O` in the reference vs. `S` in the generated code where name referance starting position on board so S is good prediction), showing lacking knowledge about program inputs, but working it out with an quite good approximation.

### Example Model Outputs
**UDP Server Code:**
- **Expected:** `data, address = sock.recvfrom(4096)`
  	`print(f"Received message: {data} from {address}")`
- **Predicted:** `print(f"Sent {sent} bytes to {address}")`
  	`else:`
  	`print("No data from {address}")`

**Algorithm Code:**
- **Expected:** `start_x, start_y = i, j`
  	`break`
- **Predicted:** `print(solve(board, S, start_x, start_y))`

- **Expected:** `class Direction(Enum):`
  	`P = (0, 1)`
  	`G = (-1, 0)`
- **Predicted:** `class Direction(Enum):`
  	`L = (0, -1)`
  	`D = (1, 0)`

These examples illustrate that CodeLlama was close to an exact match but differed in minor ways such as naming conventions and structural choices.

## Conclusion
- CodeLlama outperformed Tiny StarCoder in both tasks, particularly in algorithmic problem-solving, which is understandable as its bigger model and required to use GPU while Tiny StarCoder can perform on CPU.
- Tiny StarCoder struggled significantly with the UDP server task.
- Neither model produced exact matches, but ChrF scores indicate partial conceptual understanding.
- CodeLlama was able to approximate expected implementations but sometimes introduced inefficiencies or incorrect logic.
- The dataset structure provided useful context, allowing models to generate code with a reasonable understanding of surrounding logic.

These findings suggest that while AI models can grasp high-level coding patterns, they still struggle with precise and optimized implementations, particularly in more specialized domains such as networking. Future evaluations could explore how dataset modifications affect performance and how models handle longer code dependencies.

It is particularly interesting that I labeled the UDP server file as simple_file.py, assuming it would be an easier task, whereas the algorithmic problem, which requires some level of reasoning and understanding, turned out to be significantly easier for the model to replicate. This suggests that structured patterns in computational problems may be more predictable for AI models than handling less structured patterns in networking tasks, but it can also mean models do not handle well tasks that rely on specific external libraries and APIs.

