# Good2Know

# user_post_api
### Pre-requirement:
- [python_instagram_api](https://github.com/ping/instagram_private_api "python_instagram_api")
- [langdetect](https://github.com/Mimino666/langdetect "langdetect")

### Usage:

python3 post_scrawler_public.py -i `<input_file_path>` -o `<output_file_path>` -p `<post_count>`

python3 post_scrawler_private.py -u `<username>` -p `<password>` -i `<input_file_path>` -o `<output_file_path>`

## CSV Tables

### Input
#### user_name.csv

Header  | user_name
------------- | -------------
&nbsp; | XXXXXXXX

### Output
#### post.csv

Header  | user_id | user_name | user_img_url | followed_by | post_count | text 
------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
&nbsp; | XXXXXXXX | XXXXXXXX | XXXXXXX | XXXXXXX | XXXXXXX | XXXXXXXX 
