import re
import os
import sys
import getopt
import hashlib

def print_help():
  print("useage: "+sys.argv[0]+" [(-i|--input) <input-file-name>] [(-o|--output) <output-file-name>]")
  exit()

global_config={}

def get_configure(argv):
  ret = {}
  base,extra = getopt.getopt(argv[1:], 'i:o:h', ['input','output','image-path','help'])
  for k,v in base:
    if k=='-h' or k=='help':
       ret['help']= True
    if k=='-i' or k=='input':
       ret['input']= os.path.abspath(v)
    if k=='-o' or k=='output':
       ret['output']= os.path.abspath(v)
    if k=='image-path':
       ret['image-path']= os.path.abspath(v)

  if ret.get('input',False)==False and len(extra)>=1:
    ret['input']= extra[0]

  if ret.get('output',False)==False:
    ret['output']= ret.get('input',False)

  if ret.get('help',False)==True or ret.get('input',False)==False:
    return print_help()
  
  ret['image-path']= ret.get('image-path', 'img')

  return ret

def gen_math_image_filename(math_exp):
  global global_config
  image_path= global_config['image-path']
  file_hash= hashlib.md5(math_exp.encode('utf8')).hexdigest()
  image_filename= os.path.join(image_path, file_hash+'.gif')
  return image_filename

def get_math_image(math_exp):
  global global_config
  output_dir= os.path.dirname(global_config['output'])
  image_path= gen_math_image_filename(math_exp)
  image_path= os.path.join(output_dir, image_path)

  wget_prefix= 'wget'
  output_name= image_path
  output_dir= os.path.dirname(image_path)
  url_prefix= 'http://latex.codecogs.com/gif.latex?'
  image_url= url_prefix + math_exp
  image_url= '"'+image_url+'"'

  os.makedirs(output_dir, exist_ok=True)
  cmd= wget_prefix+' -O '+output_name+' '+image_url

  os.system(cmd)

def translate_math_link(math_exp):
  get_math_image(math_exp)
  return '['+math_exp+']: '+gen_math_image_filename(math_exp)

def translate_link(line):
  match_result=re.match('\[(.*)\]: #(.*)', line)
  if match_result==None:
    return line
  exp= match_result.group(1).strip()
  method= match_result.group(2).strip()
  
  if method=='math':
    return translate_math_link(exp)

  # no method match
  return line

def translate_file():
  global global_config
  ifile_name= global_config['input']
  infile= open(ifile_name, 'r')
  infile_lines= infile.readlines()
  infile.close()
  outfile_lines= []

  for line in infile_lines:
    outfile_lines.append(translate_link(line))

  outile_name= global_config['output']
  outfile= open(outile_name, 'w')
  outfile.writelines(outfile_lines)
  outfile.close()
  

def main():
  global global_config
  global_config= get_configure(sys.argv)
  print(global_config)
  translate_file()

if __name__=='__main__':
  print(sys.argv)
  main()
