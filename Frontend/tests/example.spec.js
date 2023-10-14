// @ts-check
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
	await page.goto('http://172.21.112.242:5173/');
	await page.getByText("Don't have an account?").click();
	const n = Math.floor(Math.random() * 1000);
	await page.getByPlaceholder('First Name').fill('John' + n);
	await page.getByPlaceholder('Last Name').fill('Doe');
	await page.getByPlaceholder('Email').fill(`John${+n}Doe@email.com`);
	await page.getByPlaceholder('Password').first().fill('lol123sd');
	await page.getByPlaceholder('Re-Password').fill('lol123sd');
	await page.getByRole('button', { name: 'Register' }).click();
	/*
	await new Promise((res) => setTimeout(res, 500));
	*/
	await expect(page.getByRole('button', { name: 'login' })).toBeVisible();

	await page.getByPlaceholder('Email').fill(`John${+n}Doe@email.com`);
	await page.getByPlaceholder('Password').first().fill('lol123sd');
	await page.getByRole('button', { name: 'Login' }).click();
	await expect(page.getByRole('heading', { name: 'Hello Jan Palma!' })).toBeVisible();

	await new Promise((res) => setTimeout(res, 500));

	await page.getByRole('button', { name: 'Open' }).first().click();
});
/*
test('get started link', async ({ page }) => {
	await page.goto('https://playwright.dev/');

	// Click the get started link.
	await page.getByRole('link', { name: 'Get started' }).click();

	// Expects page to have a heading with the name of Installation.
	await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});*/
