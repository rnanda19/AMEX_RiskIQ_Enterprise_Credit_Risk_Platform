.PHONY: install test test-all lint format-check syntax-check clean help

PROBLEMS := Problem1_Credit_Scoring_PD_Prediction \
            Problem2_Risk_Tier_Classification \
            Problem3_Expected_Credit_Loss_IFRS9_CECL \
            Problem4_Delinquency_Escalation_Loss_Severity \
            Problem5_Early_Payment_Default_Detection \
            Problem6_Dynamic_Behavioral_Credit_Scoring \
            Problem7_Early_Warning_System \
            Problem8_Roll_Rate_Modeling

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
