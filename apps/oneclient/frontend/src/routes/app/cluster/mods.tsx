import type { ModpackFile } from '@/bindings.gen';
import type { ModCardContextApi } from '@/components';
import { ModCardContext, ModList } from '@/components';
import { bindings } from '@/main';
import { useCommandSuspense } from '@onelauncher/common';
import { createFileRoute } from '@tanstack/react-router';
import { OverlayScrollbarsComponent } from 'overlayscrollbars-react';
import { useMemo } from 'react';

export const Route = createFileRoute('/app/cluster/mods')({
	component: RouteComponent,
});

export function getFilePackageType(file: ModpackFile) {
	if ('Managed' in file.kind)
		return file.kind.Managed[0].package_type;
	return file.kind.External.package_type;
}

function RouteComponent() {
	const { cluster } = Route.useRouteContext();
	const { data: bundles } = useCommandSuspense(['getBundlesFor', cluster.id], () => bindings.oneclient.getBundlesFor(cluster.id));
	const { data: installedPackages } = useCommandSuspense(['getLinkedPackages', cluster.id], () => bindings.core.getLinkedPackages(cluster.id));

	const filteredBundles = useMemo(() =>
		bundles.map(b => ({
			...b,
			manifest: { ...b.manifest, files: b.manifest.files.filter(f => getFilePackageType(f) === 'mod') },
		})), [bundles]);

	const context = useMemo<ModCardContextApi>(() => ({
		enableClickToDownload: true,
		installedPackages,
	}), [installedPackages]);

	if (filteredBundles.every(b => b.manifest.files.length === 0))
		return <p className="p-4 text-fg-secondary">No mods found in {cluster.name}</p>;

	return (
		<OverlayScrollbarsComponent className="bg-none">
			<div className="min-h-148">
				<ModCardContext.Provider value={context}>
					<ModList bundles={filteredBundles} cluster={cluster} />
				</ModCardContext.Provider>
			</div>
		</OverlayScrollbarsComponent>
	);
}
