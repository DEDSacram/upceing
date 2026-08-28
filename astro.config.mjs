// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
			customCss: [
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'Year 1: Required',
					items: [
						{
							label: 'Winter Semester (ZS)',
							items: [{ autogenerate: { directory: 'year-1-required/winter' } }]
						},
						{
							label: 'Summer Semester (LS)',
							items: [{ autogenerate: { directory: 'year-1-required/summer' } }]
						}
					]
				},
				{
					label: 'Year 1: Optional Required',
					items: [
						{
							label: 'Winter Semester (ZS)',
							items: [{ autogenerate: { directory: 'year-1-optional/winter' } }]
						},
						{
							label: 'Summer Semester (LS)',
							items: [{ autogenerate: { directory: 'year-1-optional/summer' } }]
						}
					]
				},
				{
					label: 'Optional Courses',
					items: [
						{
							label: 'Winter Semester (ZS)',
							items: [{ autogenerate: { directory: 'optional/winter' } }]
						},
						{
							label: 'Summer Semester (LS)',
							items: [{ autogenerate: { directory: 'optional/summer' } }]
						}
					]
				}
			],
		}),
	],
});