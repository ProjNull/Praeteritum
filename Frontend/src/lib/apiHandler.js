import { PUBLIC_API_URL } from '$env/static/public';
import { sha256 } from 'js-sha256';

export class EndpointFormatError extends Error {
	/**
	 *
	 * @param {string} message Error message
	 */
	constructor(message) {
		super(message); // (1)
		this.name = 'ValidationError'; // (2)
	}
}

export class TokenError extends Error {
	/**
	 *
	 * @param {string} message Error message
	 */
	constructor(message) {
		super(message); // (1)
		this.name = 'TokenError'; // (2)
	}
}

export default class APIHandler {
	/**
	 * @description Api Request Handler
	 * @param {string} [token] Optional token data (can be changed with 'setToken(token)') 
	 */
	constructor(token) {
		if (!PUBLIC_API_URL.endsWith('/')) {
			this.url = PUBLIC_API_URL + '/';
		} else {
			this.url = PUBLIC_API_URL;
		}
		if (token) {
			this.token = token
		}
	}
	/**
	 * @description Universal api request (Not recommended for production)
	 * @param {string} url Endpoint url (without api url)
	 * @returns {Promise<Object>} retu
	 */
	async uniFetch(url) {
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat(url));
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}
	
	async login(email, password) {
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat("login"), {
				method:"post",
				headers: {
					"Content-Type":"application/json"
				},
				body: `{
					"email": "${email}",
					"password": "${password}"
				}`
			});
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}

	async register(email, password,display) {
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat("register"), {
				method:"post",
				headers: {
					"Content-Type":"application/json"
				},
				body: `{
					"email": "${email}",
					"password": "${password}",
					"displayname": "${display}"
				}`
			});
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}
	setToken(token) {
		this.token = token
	}

	async fetchBoards(group) {
		if (!this.token) {
			throw new TokenError("Token Not set")
		}
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat("fetchBoards"), {
				method:"post",
				headers: {
					"Content-Type":"application/json"
				},
				body: `{
					"Group_ID": "${group}"
				}`
			});
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}

	async profile() {
		if (!this.token) {
			throw new TokenError("Token Not set")
		}

		
		
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat("fetchBoards"), {
				method:"get",
			});
			const responce = await responceRaw.json();
			const email = responce[""].toLowerCase().replace(/\s/g, '');
			const hashedEmail = sha256(email);
			return {
				...responce, avatar: hashedEmail
			};
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}

	async getQuestions(id) {
		if (!this.token) {
			throw new TokenError("Token Not set")
		}

		
		
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat(`questions_for/${id}`), {
				method:"get",
				headers: {
					"Authorization": this.token
				}
			});
			const responce = await responceRaw.json();
			return responce.questions;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}

	async fetchFeedbacks(Qid) {
		if (!this.token) {
			throw new TokenError("Token Not set")
		}

		
		
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat(`fetchFeedbacks`), {
				method:"post",
				headers: {
					"Authorization": this.token,
					"content-type": "application/json"
				},
				body: `{"Question_ID": ${Qid + 1}}`
			});
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}

	async sendFeedback(text,col,qID) {
		if (!this.token) {
			throw new TokenError("Token Not set")
		}

		
		
		try {
			const responceRaw = await fetch(this.url + this.endpointFormat(`sendFeedback`), {
				method:"post",
				headers: {
					"Authorization": this.token,
					"content-type": "application/json"
				},
				body: `{"Content": "${text}",
				"ColumnName": "${col}","Question_ID": ${qID + 1}}`
			});
			const responce = await responceRaw.json();
			return responce;
		} catch (error) {
			throw new Error('Fetch error: ' + error);
		}
	}
	/**
	 * @description Checks and formats endpoint url.
	 * @throws {Error} Errors out if
	 * @param {string} endpoint Unformated endpoint
	 * @returns {string} Formated endpoint
	 */
	endpointFormat(endpoint) {
		if (endpoint.endsWith('/')) {
			endpoint = endpoint.slice(0, -1);
		}
		if (endpoint.startsWith('/')) {
			endpoint = endpoint.slice(1);
		}
		return endpoint;
	}
}
