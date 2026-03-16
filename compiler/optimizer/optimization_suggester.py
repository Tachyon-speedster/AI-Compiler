def suggest_optimizations(patterns):

    suggestions = []

    for p in patterns:

        if p["pattern"] == "Arithmetic Summation Loop":

            suggestions.append({
                "message": "Loop can be replaced with mathematical formula",
                "improvement": "Use n(n-1)/2",
                "new_complexity": "O(1)"
            })

        elif p["pattern"] == "Nested Loop":

            suggestions.append({
                "message": "Nested loops detected",
                "improvement": "Consider hash-based lookup or better algorithm",
                "new_complexity": "O(n)"
            })

    return suggestions
