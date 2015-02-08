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

  if ret.get('help',False)==True:
    return print_help()

  if ret.get('input',False)==False and len(extra)>=1:
    ret['input']= extra[0]

  if ret.get('input',False)==False:
    return print_help()

  if not os.path.exists(ret['input']):
    print('can not find file at: ', os.path.abspath(ret['input']))
    print('======')
    return print_help()

  if ret.get('output',False)==False:
    if len(extra)>=2:
      ret['output']= extra[1]
    else:
      ret['output']= ret.get('input',False)
  
  ret['image-path']= ret.get('image-path', 'img')

  return ret

def gen_dirname_from_filename(filename):
  print('gen_dirname_from_filename: ', filename)
  return filename+'.d'

def gen_math_image_filename(math_exp, image_dir):
  file_hash= hashlib.md5(math_exp.encode('utf8')).hexdigest()
  image_filename= os.path.join(image_dir, file_hash+'.gif')
  return image_filename

def wget_math_image(math_exp, image_output_filename):
  wget_prefix= 'wget'

  url_prefix= 'http://latex.codecogs.com/gif.latex?'
  image_url= url_prefix + math_exp
  image_url= '"'+image_url+'"'

  os.makedirs(os.path.split(image_output_filename)[0], exist_ok=True)
  cmd= wget_prefix+' -O "'+image_output_filename+'" '+image_url

  os.system(cmd)

def translate_math_link(math_exp):
  global global_config
  image_output_dirname= gen_dirname_from_filename(global_config['output'])
  _,output_filename= os.path.split(global_config['output'])
  image_output_dirname_base_on_output_file_path= gen_dirname_from_filename(output_filename)
  image_output_filename= gen_math_image_filename(math_exp, image_output_dirname)
  wget_math_image(math_exp, image_output_filename)

  return '['+math_exp+']: "'+ \
    gen_math_image_filename(math_exp, image_output_dirname_base_on_output_file_path) + \
    '"'

def translate_link(line):
  match_result= re.match('\[(.*)\]: #(.*)', line)
  if match_result==None:
    return line
  exp= match_result.group(1).strip()
  method= match_result.group(2).strip()
  
  if method=='math':
    return translate_math_link(exp)

  # no method match
  return line

def translate_file(ifile_name, ofile_name):
  global global_config
  global_config['input']= ifile_name
  global_config['output']= ofile_name
  print('translate_file(', ifile_name, ',', ofile_name, ')')
  infile= open(ifile_name, 'r')
  infile_lines= infile.readlines()
  infile.close()

  outfile_lines= []
  for line in infile_lines:
    outfile_lines.append(translate_link(line))

  outfile= open(ofile_name, 'w')
  outfile.writelines(outfile_lines)
  outfile.close()
  
def translate(ifile_path, ofile_path):
  print('translate(', ifile_path, ',', ofile_path, ')')
  if os.path.isfile(ifile_path):
    # ifile_path is file
    if len(os.path.split(ofile_path)[1])!=0:
      # ofile_path is not a dir path
      translate_file(ifile_path, ofile_path)
    else:
      _,filename= os.path.split(ifile_path)
      translate_file(ifile_path, os.path.join(ofile_path, filename))
  else:
    # ifile_path is dir
    for item in os.listdir(ifile_path):
      cur_ifile_path= os.path.join(ifile_path, item)
      cur_ofile_path= os.path.join(ofile_path, item)
      translate(cur_ifile_path, cur_ofile_path)
    

def main():
  global global_config
  global_config= get_configure(sys.argv)

  translate(global_config['input'], global_config['output'])

if __name__=='__main__':
  print(sys.argv)
  main()
