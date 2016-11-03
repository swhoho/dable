# dable
Word2Vec Project
Hojung Yeo
swhoho@gmail.com

^: must read sign


Note : Purpose of this project is pratice for creating news recommendation system.
       ^To test my project please run 1.~3. through server and 4 by using ipython.

 
1.
-create_table.py : Code to create new tables in MySQL
                ^(Please change! server = '' and connection_string ='' Name of schema must be "Test")
2.
-crawler2.py : code for crawling IT News and comment from Naver
              ^(change server = ')

                                                                       
3.
-news_rec.ipynb
          reason for making this file .ipynb(not .py) is due to the server cpu problem.
          Since coding process require heavy work on cpu, it might not work in your server.
          run this program to save similarities between news.
          
 
                
4.
-webserver.py : API function
            ^(change server = ')
            
            
              (1) @app.route('/') test whether api function normally  result must be Hi, Dable
              (1.1)@app.route('/test')  result must be 'name' : 'Hojung', 'family' : 'Yeo'
              (2)@app.route('/auth') Code to practice redis and user info save ()
                                    /auth?user= * must give your api password to operate (3) normally
                                    *ID can be any combination of characters
                                    
              (3)@app.route('/news/search/<keyword>')?user=*&apikey= "result from (2)"
                                    result must give news that relate with keyword 
                                    ** run (2) first
                                    
              (4)@app.route('/news/recent') result must be title and content of top top 5 recent news
              
              (5)
              @app.route('/comment/search/<keyword>')?page=*&pagesize=**
                                    based on the page # and pagesize, this function provied comments that realted to keyword
                                    * number of pages
                                    ** number of comments in * page
                                    
                                      
              (6)
              @app.route('/news/rec')?url=*
                                  based on word2vec, result provides you related news of *
                                  * can be url or the aid number**  (ex)aid = 0008797715)
                                  ** aid number is the last 10 digit of IT News url.
                                  please check use your similarity table data to perform this api.
                                  
(do not run/operate files below)
-newsdao.py : code to save and operate api function from webserver.py 
              ^(change server = ')
              
-model.py: sqlalchemy.ext.declarative setting the table form of sqlalchemy
-memcache.py : change server name and check port
              ^(change server = ')
              




P.S:
Please disregard some functions,Block Comment Remark that is not relate to operate.
The reason of leaving Block Comment Remarks -- check 3.
