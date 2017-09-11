all:
	python3 tools/wget-math-image.py src output

clean:
	rm -r output/