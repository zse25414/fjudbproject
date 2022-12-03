import re
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, jsonify
from time import time
import pymysql

from config import CONFIG

USERS = {}
TOKENS = {}

app =Flask(name)
@app.route('/')
def home():
    return '<h1>Hello </h1>'

@app.route('/api/v1/asd', methods=['GET','POST'])
def get_prodctsNutrition_labelling():
    connection = pymysql.connect(**CONFIG)
    json = request.get_json()
    # Check if input data are valid
    checkParams = ["name"]
    for param in checkParams:
        if param not in json:
            return jsonify({
                'status':'error',
                'message':f'Input data {param} is not valid'
            }), 400
    name = json['name']
    with connection.cursor() as cursor:
            sql = "SELECT name FROM product WHERE name like %s;"
            cursor.execute(sql, ('%'+(name)+'%'))
            results = cursor.fetchall()
            #print(arrname)
            if results is None:
                return jsonify({
                    'status':'error',
                    'message':'Product not found'
                }), 404
            products = []
            for result in results:
                product = {
                    'name':result[0]
                }
                products.append(product)
            return jsonify({
                'status':'success',
                'message':'User data found',
                'data': products
            })

@app.route('/post-value', methods=['POST'])
def post_value():
    # 方法 1
    return request.args['input_value']

    # 方法 2, 不帶預設值
    return request.args.get('input_value')

    # 方法 2, 帶預設值
    return request.form.get('input_value', 'No input')

if name == "main":

    app.run(debug=True)