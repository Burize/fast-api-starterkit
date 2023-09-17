import {expect, test} from '@jest/globals';
import {DefaultService} from './api_client';
import {v4 as uuid} from 'uuid';
import {CookieJar} from 'tough-cookie';

import {OpenAPI} from "./api_client";
import axios from "axios";
import {wrapper} from "axios-cookiejar-support";

OpenAPI.BASE = 'http://127.0.0.1:8000';


const cookieJar = new CookieJar();
const api = wrapper(
    axios.create({
      baseURL: 'http://127.0.0.1:8000/api',
      withCredentials: true,
      jar: cookieJar,
    })
  );

test('User can add a new order', async () => {
    const username = `test_${uuid()}`;
    const password = '1234';
    await DefaultService.createApiUserPost({
        username,
        password,
        email: `test_${uuid()}@email.com`,
    });

    // openapi-typescript-codegen does not provide response headers to get session cookies
    // and does not allow set a cookies for next request, so axios with cookiejar support is used further
    await api.post('/authenticate/login', {username, password});

    const description = uuid();
    const createdOrderResponse = await api.post('/order', {description})
    const orderId = createdOrderResponse.data['id']

    const ordersResponse = await api.get('/order')

    expect(ordersResponse.data).toEqual([{
        description,
        id: orderId,
        number: 1,
    }])

})