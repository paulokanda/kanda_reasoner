"""Support missing-docstring insertion workflows."""

import asyncio

class PollingService:
    async def fetch_once(self, delay_seconds: float) -> str:
        await asyncio.sleep(delay_seconds)
        return "done"

    async def fetch_many(self, count: int) -> list[str]:
        results = []
        for _ in range(count):
            results.append(await self.fetch_once(0))
        return results
