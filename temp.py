@app.route("/search",methods=['GET','POST'])
def search( ):
    '''
    search page
    '''
    info = request.form.get('info')
    PER_PAGE = 1 #每一页显示的结果数目
    results = food120tab.query.filter(food120tab.proname.like("%{0}%".format(info)))
    pagination = results.paginate(1, PER_PAGE, False)
    records =pagination.items
    return render_template("result.html",pagination=pagination,records=records)