##################################################################### 
## Author: Pavel Gordeyev
## Date: 8/10/20
## Description:  Google Question: Given a number N, write a code to
##				 print all positive numbers less than N in which all
##				 adjacent digits differ by 1.
##
##				 This solution uses a dynamic programming approach
##				 to save all previously found values to an array.
##				 These values are then used to create new values
##				 since it will be repeating as the numbers get
##				 larger.  We are only concerned with the first
## 				 and second digits of any number.  If these differ
##				 by 1, and this implies that all the other digits
##				 in the number will differ by 1 from each other
##				 since they were previously found to comply with this
##			     property.  There are a few special cases, but the
##				 effect on the runtime is neglible.  The solution
##				 was tested successfully on a value as large as 
##				 2,500,000,000,000,000,000,000.
#####################################################################
import sys

def main():

	# Get the user's input
	n = int(sys.argv[1])

	# Validate user input
	if n < 0:
		print ("Invalid entry. n must be >= 0")
		return

	# Initialize the array to store values
	arr = []

	# Initialize counter to 0
	i = 0

	# Get an array for all the single digits, ie <10
	while i < n and i < 10:
		arr.append(i)
		i += 1

	# Step through values >= 10
	if n >= 10:
		
		# Loop through values, with each i being a power of 10, ie 10,100,1000,etc
		while i < n:

			# Use j to loop through the intermediary values with increments of i
			# Example, i = 100, j = 100, 200, 300..
			# Adds previously found values based on the digit to j to generate the true value
			j = i
			while j < n and j < i * 10:

				# Values below 100
				if j < 100:

					# Appends new values in sorted order

					# Find the first digit - 1; 0 if first digit is 1
					lowerAdj = max(j // 10 - 1, 0)

					# Check that the sum of j & value is lower than the requested n
					if j + lowerAdj < n:
						arr.append(j + lowerAdj)

						# Find the first digit + 1
						upperAdj = j // 10 + 1 

						# Check that value itself is < 10 
						# Check that the sum of j & value is lower than the requested n
						if upperAdj < 10 and j + upperAdj < n:
							arr.append(j + upperAdj)
				
				# All other values >= 100
				else:

					# Special case where first digit is 1
					if j // i == 1:

						# Get values in the existing array that are powers of 10 to add to j
						# This occurs for values like 101, 1010, 1012, 10101, etc.
						vals = getValsBounded(arr,10**(getDigits(j)-3),10**(getDigits(j)-3))

						# Add each value to j and append it to the array
						appendAllValues(arr,vals,j,n)

						# Find the values where their first digit = the current first digit + 1
						vals = getValsBounded(arr,(j // i + 1) * i / 10,i/10)

						# Add each value to j and append it to the array
						appendAllValues(arr,vals,j,n)
						
					# All other values where the first digit is > 1
					else:

						# Find the values where their first digit = the current first digit - 1
						vals = getValsBounded(arr,(j // i - 1) * i / 10,i/10)

						# Add each value to j and append it to the array
						appendAllValues(arr,vals,j,n)

						# Special case for values starting with 9 as the first digit
						if j // i + 1 < 10:

							# Find the values where their first digit = the current first digit + 1
							vals = getValsBounded(arr,(j // i + 1) * i / 10,i/10)

							# Add each value to j and append it to the array
							appendAllValues(arr,vals,j,n)

				j += i

			i *= 10

	# Generate the output string
	outputStr = ""

	for i in range(0,len(arr)):
		
		outputStr += str(arr[i])

		if i < len(arr) - 1	:
			outputStr += ", "

	# Print the result
	print(outputStr)

#####################################################################
## Description:  Appends all values in vals array to arr
#####################################################################
def appendAllValues(arr,vals,x,n):

	for val in vals:
		if x + val < n:
			arr.append(x + val)

#####################################################################
## Description:  Returns the number of digits in n
#####################################################################
def getDigits(n):

	count = 0

	# Divide by 10 until quotient is 0
	while n > 0:
		n = n // 10
		count += 1

	return count

#####################################################################
## Description:  Returns the values in array between the lower
##				 and upper bounds of the first digit of the key.
##				 Lower is inclusive and upper is exclusive.
#####################################################################
def getValsBounded(arr,key,div):

	lower = lBound(arr,key,0,len(arr)-1,div)
	upper = uBound(arr,key,0,len(arr)-1,div)

	return arr[lower:upper]

#####################################################################
## Description:  Returns the lower bound of where to find the
##			     values in the arr with the first digit of the key.
##				 This is an adaption of the binary search.
#####################################################################
def lBound(arr,key,low,high,div):

	# Check base case
	if high >= low:

		# Determine the midpoint of the array
		mid = low + (high - low) // 2

		# Quotient of key / div is less than or equal to the quotient of middle element / div
		if arr[mid] // div >= key // div:
			return lBound(arr,key,low,mid - 1,div)

		# Quotient of key / div is greater than the quotient of middle element / div
		else:
			return lBound(arr,key,mid + 1,high,div)

	# Element is not found in the array
	return low

#####################################################################
## Description:  Returns the upper bound of where to find the
##			     values in the arr with the first digit of the key.
##				 This is an adaption of the binary search.
#####################################################################
def uBound(arr,key,low,high,div):

	# Check base case
	if high >= low:

		# Determine the midpoint of the array
		mid = low + (high - low) // 2

		# Quotient of key / div is less than to the quotient of middle element / div
		if arr[mid] // div > key // div:
			return uBound(arr,key,low,mid - 1,div)

		# Quotient of key / div is greater than or equal to the quotient of middle element / div
		else:
			return uBound(arr,key,mid + 1,high,div)

	# Element is not found in the array
	return low

# Call main function
if __name__ == "__main__":
	main()