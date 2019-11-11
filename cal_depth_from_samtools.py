#!/usr/bin/python
import re,argparse


parser = argparse.ArgumentParser(description='Calculate depth by particular window size')
parser.add_argument("-i", "--input", help="output from samtools depth program", required=True)
parser.add_argument("-w", "--window_size", help="window size", type=int, required=True)
parser.add_argument("-s", "--step_size", help="step size", type=int, required=True)
parser.add_argument("-o", "--output", help="output path and file name", required=True)
args = parser.parse_args()


def main():
	with open(args.input,"r") as input:
		input_list=input.readlines()

	
	scaf_dict={}
	chromosome=""
	chromosome_list=[]
	input_list.append("0\t0\t0")
	for line in input_list:
		re.sub("\n","",line)
		line_list=line.split()
		if line_list[0] != chromosome:
			scaf_dict[chromosome]=chromosome_list
			chromosome=line_list[0]
			chromosome_list=[]
			chromosome_list.append(line_list[2])
		else:
			chromosome_list.append(line_list[2])
	del scaf_dict[""]
	out=open(args.output,"a+")
	out.write("Chr\t"+"Start\t"+"End\t"+ "Depth\n")
	for chr in scaf_dict.keys():
		chromosome_window_depth=average_depth(chr, scaf_dict)
		out.write(chromosome_window_depth)

	out.close()


def average_depth (chr, scaf_dict):
	i=0
	chr_length=len(scaf_dict[chr])
	start=1
	end=""
	final_list=[]
	sum=0

	while start <= chr_length - args.window_size:
		if i < args.window_size:
			sum=sum+int(scaf_dict[chr][start+i-1])
			i=i+1
		else:
			end=start+i-1
			depth=sum/args.window_size
			final_list.append(chr+"\t"+str(start)+"\t"+str(end)+"\t"+str(depth)+"\n")
			sum=0
			start=start+args.step_size
			i=0

	while i <= chr_length - start:
		if i < chr_length - start:
			sum=sum+int(scaf_dict[chr][start+i-1])
			i=i+1
		else:
			sum=sum+int(scaf_dict[chr][start+i-1])
			end=start+i
			depth=sum/args.window_size
			final_list.append(chr+"\t"+str(start)+"\t"+str(end)+"\t"+str(depth)+"\n")	
			i=i+1

	final=""
	for a in final_list:
		final=final+a
	return final


if __name__ == "__main__":
   	main()
