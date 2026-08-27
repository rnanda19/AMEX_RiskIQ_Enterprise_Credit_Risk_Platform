.PHONY: install test test-all lint format-check syntax-check clean help

PROBLEMS := 01_Problem1_Credit_Scoring_PD_Prediction \
            02_Problem2_Risk_Tier_Classification \
            03_Problem3_Expected_Credit_Loss_IFRS9_CECL \
            04_Problem4_Delinquency_Escalation_Loss_Severity \
            05_Problem5_Early_Payment_Default_Detection \
            06_Problem6_Dynamic_Behavioral_Credit_Scoring \
            07_Problem7_Early_Warning_System \
            08_Problem8_Roll_Rate_Modeling \
            09_Problem9_Collections_Optimization \
            10_Problem10_Credit_Line_Management \
            11_Problem11_Real_Time_Portfolio_Monitoring \
            12_Problem12_360_Customer_Intelligence \
            13_Problem13_Risk_Adjusted_Profitability_Modeling \
            14_Problem14_Executive_Decision_Support_Dashboard

help:
	@echo "Targets:"
	@echo "  install        Install dev/CI dependencies + shared/ in editable mode"
	@echo "  test           Run shared/ tests only (fast)"
	@echo "  test-all       Run shared/ + every Problem's tests (what CI runs)"
	@echo "  lint           pyflakes across shared/, scripts/, every Problem's src/+tests/"
	@echo "  syntax-check   ast.parse every notebook code cell (scripts/check_notebook_syntax.py)"
	@echo "  clean          Remove __pycache__/.pytest_cache clutter"

install:
	pip install -r requirements-dev.txt
	pip install -e . --no-deps

test:
	python -m pytest shared/tests -v

test-all:
	python -m pytest shared/tests $(foreach p,$(PROBLEMS),$(p)/tests) -v

lint:
	pyflakes shared/ scripts/ $(foreach p,$(PROBLEMS),$(p)/src $(p)/tests)

syntax-check:
	python scripts/check_notebook_syntax.py .

clean:
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
