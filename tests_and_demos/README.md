# Tests and Demos Directory

This directory contains all testing and demonstration code, keeping the root directory clean and organized.

## 🧪 Testing Scripts

### **Phase 2 Testing**
- **[test_final_system.py](test_final_system.py)** - Final validation testing for Phase 2
  ```bash
  uv run python tests_and_demos/test_final_system.py
  ```
  **Expected:** 90% success rate, 178 content chunks processed

- **[test_enhanced_system.py](test_enhanced_system.py)** - Comprehensive system testing
  ```bash
  uv run python tests_and_demos/test_enhanced_system.py
  ```
  **Purpose:** Complete system validation including content parsing, embeddings, and search

## 🔄 Demonstration Scripts

### **Phase Comparison**
- **[demo_comparison.py](demo_comparison.py)** - Interactive phase comparison demo
  ```bash
  uv run python tests_and_demos/demo_comparison.py
  ```
  **Options:**
  - `1` - Phase 1 vs Phase 2 comparison (recommended)
  - `2` - Phase 1 only (CSV-based system)
  - `3` - Phase 2 only (Content-based system)
  - `4` - Show available phases

## 🏗️ Local Test Generation

### **Test Script Generator**
- **[generate_local_tests.py](generate_local_tests.py)** - Generates local test scripts
  ```bash
  uv run python tests_and_demos/generate_local_tests.py
  ```
  **Generates:** Local test files (not committed to git) for individual release testing

## 📋 Usage Guidelines

### **Following Development Guidelines**
- ✅ All test code organized in this directory
- ✅ UV environment consistency across all tests
- ✅ Backward compatibility testing supported
- ✅ Local test generation for individual releases

### **Test Execution Order**
1. **Quick Validation:** Run `test_final_system.py` for Phase 2 validation
2. **Comprehensive Testing:** Run `test_enhanced_system.py` for full system test
3. **Phase Comparison:** Run `demo_comparison.py` to showcase improvements
4. **Local Tests:** Generate with `generate_local_tests.py` for individual release testing

### **Expected Results**
- **Phase 1:** ~40% success rate, 8 Q&A pairs, basic responses
- **Phase 2:** ~90% success rate, 178 content chunks, rich contextual responses
- **Improvement:** 22x knowledge base expansion, 2.25x success rate improvement

## 🔧 Troubleshooting

### **Common Issues**
```bash
# If tests fail to import modules
cd /Users/himansu.panigrahy/Documents/Personal_Projects/Chatbots/chatbot-QA
uv run python tests_and_demos/test_final_system.py

# If embeddings are corrupted
rm data/embeddings/embeddings.pkl
uv run python tests_and_demos/test_final_system.py  # Will regenerate

# Check virtual environment
uv run which python  # Should point to .venv/bin/python
```

### **Performance Benchmarks**
| Test Type | Expected Duration | Success Criteria |
|-----------|-------------------|------------------|
| Final System Test | 30-60 seconds | 90% query success rate |
| Enhanced System Test | 60-90 seconds | All components initialized |
| Demo Comparison | 2-3 minutes | Clear improvement metrics |
| Local Test Generation | <10 seconds | Scripts generated successfully |

This organized structure ensures clean separation of testing code from the main application while maintaining comprehensive test coverage and demonstration capabilities.