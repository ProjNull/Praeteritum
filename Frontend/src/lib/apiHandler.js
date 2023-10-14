import { PUBLIC_API_URL } from '$env/static/public';

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

export default class APIHandler {
	/**
	 * @description Api Request Handler
	 */
	constructor() {
		if (!PUBLIC_API_URL.endsWith('/')) {
			this.url = PUBLIC_API_URL + '/';
		} else {
			this.url = PUBLIC_API_URL;
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
